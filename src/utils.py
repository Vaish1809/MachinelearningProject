#all functions in this file are used to process the data

import os
import sys  
from dataclasses import dataclass
import pandas as pd 
import numpy as np
from src.exception import CustomException
from src.logger import logging
import dill
def save_object(file_path:str, obj: object):
    """
    This function saves an object to a file using pandas.
    
    Parameters:
    - file_path (str): The path where the object will be saved.
    - obj (object): The object to be saved.
    """
    try:
        dir_path = os.path.dirname(file_path)

        os.makedirs(dir_path, exist_ok=True)
        logging.info(f"Creating directory at {dir_path} if it does not exist.")
        
        with open(file_path, 'wb') as file_obj:
            dill.dump(obj, file_obj)
       
    except Exception as e:
        raise CustomException(e, sys) from e