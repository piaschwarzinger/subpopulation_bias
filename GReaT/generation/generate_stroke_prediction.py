import pandas as pd
import logging
from be_great.utils import set_logging_level
from generate_utils import start_generation

logger = set_logging_level(logging.INFO)

""" 
    Enter the name of the folder in which the results should be stored. Alternatively adapt the path manually to read the input file. 
    If you want to drop columns, add them to the list.
    Optionally define the number of epochs, batch_size and the target column. 
"""

folder_name = "stroke_prediction"
file_path = f"./{folder_name}/{folder_name}.csv"
drop_columns_list = []

epochs = 250
batch_size = 32
conditional_column = "stroke"

data = pd.read_csv(filepath_or_buffer = file_path)
start_generation(data, folder_name, drop_columns_list, epochs, batch_size, conditional_column)
