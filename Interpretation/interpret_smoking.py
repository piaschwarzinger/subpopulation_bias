import glob

import pandas as pd
from interpret_util import start_analysis

""" 
    Define the path of the file containing the rules, 
    the folder name under which the analysis should be saved and
    the recall filter which excludes all rules below that value from the analysis.
"""

file_path_rules = "../Misprediction_Diagnoser/analysis/diagnosis_result_smoking.csv"
folder_name = "smoking"
recall_filter = 0.1

data_rules = pd.read_csv(filepath_or_buffer = file_path_rules)
start_analysis(data_rules, folder_name, recall_filter)

