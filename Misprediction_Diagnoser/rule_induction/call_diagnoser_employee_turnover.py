from call_diagnoser_util import start_diagnosis
from rule_induction.diagnoser import Settings

"""
Define the path to the files containing samples (without the number suffix) as well as the target value in the 
target column which will be mapped to True. Optionally add the conversion and map dictionary to correct types and enhance
readability of the data. Specify the number of rules returned or other settings of MD and the relevant_attributes 
according to their type - D (discrete), I (Int), C (Continuous). 
Finally define the name of the resulting file for storage purposes. 
"""

file_path = "../../GReaT/generation/employee_turnover/employee_turnover_samples"
target_value = 1.0
target_column = "event"
conversion_dict = {"int": ["age"]}
config = Settings(num_rules=5)
relevant_attributes = {
        "stag":"C",
        "gender":"D",
        "age":"I",
        "industry":"D",
        "profession":"D",
        "traffic":"D",
        "coach":"D",
        "head_gender":"D",
        "greywage":"D",
        "way":"D",
        "extraversion":"C",
        "independ":"C",
        "selfcontrol":"C",
        "anxiety":"C",
        "novator":"C"
    }
result_name = "employee_turnover"

""" Diagnosis procedure starts here """
start_diagnosis(file_path, target_column, target_value, config,relevant_attributes, result_name, conversion_dict)