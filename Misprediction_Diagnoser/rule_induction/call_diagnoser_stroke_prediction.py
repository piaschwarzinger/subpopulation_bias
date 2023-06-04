from call_diagnoser_util import start_diagnosis
from rule_induction.diagnoser import Settings

"""
Define the path to the files containing samples (without the number suffix) as well as the target value in the 
target column which will be mapped to True. Optionally add the conversion and map dictionary to correct types and enhance
readability of the data. Specify the number of rules returned or other settings of MD and the relevant_attributes 
according to their type - D (discrete), I (Int), C (Continuous). 
Finally define the name of the resulting file for storage purposes. 
"""

file_path = "../../GReaT/generation/stroke_prediction/stroke_prediction_samples"
target_value = 1.0
target_column = "stroke"
conversion_dict = {"int": ["id","age","hypertension","heart_disease", "stroke" ]}
config = Settings(num_rules=5)
relevant_attributes = {
        "age": "I",
        "ever_married": "D",
        "id": "I",
        "gender":"D",
        "work_type":"D",
        "avg_glucose_level": "C",
        "hypertension": "I",
        "heart_disease":"I",
        "bmi":"C",
        "smoking_status": "D",
        "Residence_type":"D",
    }
result_name = "stroke_prediction"

""" Diagnosis procedure starts here """
start_diagnosis(file_path, target_column, target_value, config,relevant_attributes, result_name, conversion_dict)
