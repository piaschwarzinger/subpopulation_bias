import glob
import pandas as pd
from itertools import combinations
from rule_induction.diagnoser import *


def start_diagnosis(file_path: str, target_column : str, target_value : any, config : Settings, relevant_attributes : Dict[str, str],
                    result_name : str, conversion_dict : Dict[str, list] = None, map_dict : Dict[str, list] = None):
    """
    Preprocesses data and subsequently starts diagnosis procedure for all sizes of the synthetic data sets.

    Parameters
    ----------
    file_path : str
        Path to the file(s) containing synthetic data
    target_column : str
        Name of the column of interest
    target_value : any
        Value of the target that will be mapped to "True", any other value in the target_column will be mapped to "False"
    conversion_dict : Dict[str, list]
        Mapping for columns defined in the list to a certain data type
    config : Settings
        Adapts the default settings, specifically the number of rules displayed (default : 3)
    relevant_attributes : Dict[str, str]
        Mapping for all attributes to their type (D (discrete), I (Int), C (Continuous)) except the target column (default : None)
    result_name: str
        Name of the resulting file
    map_dict: Dict[str, list]
        Mapping for columns containing 0.0 and 1.0 to meaningful values (default : None)
    """
    files = sorted(glob.glob(file_path + "*.csv"))
    result_data = pd.DataFrame()
    count = 0
    for filename in files:
        data = load_file(filename, target_column, target_value)
        if conversion_dict is not None:
            data = define_types(data, conversion_dict)
        if map_dict is not None:
            data = define_targets(data,map_dict)
        result_data, count = call_diagnoser(data, result_data, config, relevant_attributes, count)

    result_data.to_csv(f"../analysis/diagnosis_result_{result_name}.csv", index=False)


def call_diagnoser(data : pd.DataFrame, result_data : pd.DataFrame, config : Settings, relevant_attributes : Dict[str, str], count : int):
    """
    Iterates through all attributes and combines up to min(4,len(relevant_attributes)+1) attributes to use them as an input for the "discover" function.
    Calls "discover" function and saves the results by adding to the result_data.

    Parameters
    ----------
    data : pd.DataFrame
        Synthetic tabular data to be analyzed
    result_data : pd.DataFrame
         Contains the (already collected) results
    config : Settings
        Adapts the default settings, specifically the number of rules displayed (default : 3)
    relevant_attributes: Dict[str, str]
         Mapping for all attributes to their type
    count : int
        Increments after each attribute combination is tested

    Returns
    -------
    Complemented result data and the incremented count
    """
    target = Target("target", True)

    for r in range(1, min(5, len(relevant_attributes) + 1)):
        for combination_keys in combinations(relevant_attributes.keys(), r):
                combination = {key: relevant_attributes[key] for key in combination_keys}
                print(combination)
                result = discover(data, target, combination, config)
                rules = result.rules
                if len(rules) == 0:
                    continue
                result = Result(rules, data, target)
                result.print()
                result_df = result.dataframe()
                pos, neg = partition(data, target)
                result_df["Target"] = len(pos) / len(data)
                result_df["Sample size"] = len(data)
                result_data = pd.concat([result_data, result_df], ignore_index=True)
                count += 1
                print(count)
                print("\n")

    return result_data, count


def load_file(file_path : str, target_column : str, target_value : any):
    """
    Loads file and drops the first column because GReaT generates an <anonymous> column.
    Maps the target value within the target column to "True" and everything else to "False and adds this as "target" column to the data frame.

    Parameters
    ----------
    file_path : str
        Path to the file to be analyzed
    target_column : str
        Name of the column of interest
    target_value : any
        Value of the target that will be mapped to "True", any other value in the target_column will be mapped to "False"

    Returns
    -------
    Adapted synthetic data file
    """
    data = pd.read_csv(filepath_or_buffer=file_path)
    data = data.drop(data.columns[0], axis=1)
    data["target"] = data[target_column].map(lambda x: map_to_bool(x, target_value))
    return data


def map_to_bool(value : any, target_value: any):
    """
    Maps the value to True if it equals the target_value.

    Parameters
    ----------
    value : any
        Value in question
    target_value : any
        Value to compare to

    Returns
    -------
    True if the equality is given, False otherwise
    """
    if value == target_value:
        return True
    else:
        return False


def define_types(data : pd.DataFrame, conversion_dict : Dict[str, list]):
    """
    Corrects types of the underlying data based on the types and columns specified in the dictionary.

    Parameters
    ----------
    data : pd.DataFrame
        Synthetic tabular data
    conversion_dict : Dict[str, list]
        Mapping for columns defined in the list to a certain data type
    Returns
    -------
    Type corrected data
    """
    for column_type, columns in conversion_dict.items():
        for column in columns:
            data[column] = data[column].astype(column_type)
    return data

def define_targets(data, map_dict):
    """
    Maps 0.0 and 1.0 to meaningful values defined in the dictionary.

    Parameters
    ----------
    data : pd.DataFrame
        Synthetic tabular data
    map_dict : Dict[str, list]
        Mapping for columns containing 0.0 and 1.0 to meaningful values (default : None)

    Returns
    -------
    Readability enhanced data
    """
    for column, values in map_dict.items():
        data[column] = data[column].apply(lambda x: values[0] if x == 0.0 else (values[1] if x == 1.0 else None))
    return data

