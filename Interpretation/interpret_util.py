import glob

import pandas as pd

def start_analysis(data: pd.DataFrame, folder_name : str, recall_filter : float = 0.1):
    """
    Drops duplicated data, calls the quantitative_comparison function for the overall data and specific sizes
    as well as saves this combined comparison.

    Parameters
    ----------
    data : pd.DataFrame
        Tabular data containing concatenated results for various sample sizes
    folder_name : str
        The name of the folder where the file should be saved
    recall_filter : float
        Cut-off value for which all below that value are excluded from the analysis (default: 0.1)
    """
    data = data.drop_duplicates()

    result_data = pd.DataFrame()
    result_data = quantitative_comparison(data, "overall", folder_name, result_data, recall_filter)
    for i, (row_value, sub_data) in enumerate(data.groupby("Sample size")):
        result_data = quantitative_comparison(sub_data, row_value, folder_name, result_data, recall_filter)
    result_data.to_csv(f"./{folder_name}/quantitative_comparison.csv", index=False)

def quantitative_comparison(data : pd.DataFrame, result_name : str, folder_name : str, result_data: pd.DataFrame, recall_filter : float = 0.1):
    """
    Extracts the top 20 rules with a recall greater than the recall_filter, saves them to a .csv file in the defined folder
    and adds them to the result.

    Parameters
    ----------
    data : pd.DataFrame
        Tabular data containing rules with corresponding precision and recall values
    result_name : str
        Name under which the results should be stored
    folder_name : str
        Folder name where the results should be saved
    recall_filter : float
        Cut-off value which excludes all rules below that recall level
    result_data : pd.DataFrame
        Contains the (already collected) results

    Returns
    -------
    Complemented result data
    """
    data = data.sort_values(by=["precision", "recall"], ascending=[False, False])

    filtered_data = data[data["recall"] > recall_filter]
    filtered_data.to_csv(f"./{folder_name}/filtered_results_{result_name}.csv", index=False)
    filtered_data = filtered_data[:20]
    filtered_data.reset_index(drop=True, inplace=True)
    filtered_data["precision"] = filtered_data["precision"].apply(lambda x: round(x, 2))
    filtered_data["recall"] = filtered_data["recall"].apply(lambda x: round(x, 2))

    result_data[f"rule {result_name}"] = filtered_data[f"rule"]
    result_data[f"precision {result_name}"] = filtered_data["precision"]
    result_data[f"recall {result_name}"] = filtered_data["recall"]

    return result_data

