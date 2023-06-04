import pandas as pd
from interpret_util import start_analysis

""" 
    Define the path of the file containing the rules, 
    the folder name under which the analysis should be saved and
    the recall filter which excludes all rules below that value from the analysis.
"""

file_path = "../Misprediction_Diagnoser/analysis/diagnosis_result_employee_turnover.csv"
folder_name = "employee_turnover"
recall_filter = 0.1

data = pd.read_csv(filepath_or_buffer = file_path)
start_analysis(data, folder_name, recall_filter)