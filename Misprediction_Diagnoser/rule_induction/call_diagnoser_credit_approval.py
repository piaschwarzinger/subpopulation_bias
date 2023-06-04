from call_diagnoser_util import start_diagnosis
from rule_induction.diagnoser import Settings

"""
Define the path to the files containing samples (without the number suffix) as well as the target value in the 
target column which will be mapped to True. Optionally add the conversion and map dictionary to correct types and enhance
readability of the data. Specify the number of rules returned or other settings of MD and the relevant_attributes 
according to their type - D (discrete), I (Int), C (Continuous). 
Finally define the name of the resulting file for storage purposes. 
"""

file_path = "../../GReaT/generation/credit_approval/credit_approval_samples"
target_value = 1.0
target_column = "Approved"
conversion_dict = {"int": ["CreditScore", "ZipCode", "Approved"]}
map_dict = {"Gender":["Female", "Male"],
            "Married":["No", "Yes"],
            "BankCustomer":["No account", "Has account"],
            "PriorDefault":["No", "Yes"],
            "DriversLicense":["No", "Yes"],
            "Employed":["No", "Yes"]}
config = Settings(num_rules=5)
relevant_attributes = {
        "Ethnicity": "D",
        "Married": "D",
        "Age": "C",
        "Gender": "D",
        "Citizen":"D",
        "CreditScore": "I",
        "YearsEmployed": "C",
        "Income": "C",
        "Employed":"D",
        "PriorDefault": "D",
        "BankCustomer": "D",
        "Industry":"D",
        "Debt": "C",
        "ZipCode":"I",
        "DriversLicense": "D",
    }
result_name = "credit_approval"

""" Diagnosis procedure starts here """
start_diagnosis(file_path, target_column, target_value, config,relevant_attributes, result_name, conversion_dict, map_dict)


