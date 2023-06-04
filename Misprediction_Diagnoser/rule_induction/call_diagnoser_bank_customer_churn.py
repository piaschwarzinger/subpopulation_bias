from call_diagnoser_util import start_diagnosis
from rule_induction.diagnoser import Settings

"""
Define the path to the files containing samples (without the number suffix) as well as the target value in the 
target column which will be mapped to True. Optionally add the conversion and map dictionary to correct types and enhance
readability of the data. Specify the number of rules returned or other settings of MD and the relevant_attributes 
according to their type - D (discrete), I (Int), C (Continuous). 
Finally define the name of the resulting file for storage purposes. 
"""

file_path = "../../GReaT/generation/bank_customer_churn/bank_customer_churn_samples"
target_value = 1.0
target_column = "churn"
conversion_dict = {"int": ["age", "tenure", "churn", "credit_score", "customer_id", "products_number"]}
map_dict = {"credit_card":["No", "Yes"],
            "active_member":["No", "Yes"]}
config = Settings(num_rules=5)
relevant_attributes = {
        "age":"I",
        "country":"D",
        "gender":"D",
        "customer_id": "I",
        "products_number":"I",
        "active_member":"D",
        "balance": "C",
        "credit_card":"D",
        "tenure": "I",
        "credit_score": "I",
        "estimated_salary":"C",
    }
result_name = "bank_customer_churn"

""" Diagnosis procedure starts here """
start_diagnosis(file_path, target_column, target_value, config,relevant_attributes, result_name, conversion_dict, map_dict)
