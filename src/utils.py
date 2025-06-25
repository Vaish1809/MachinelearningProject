#all functions in this file are used to process the data

import os
import sys  
from dataclasses import dataclass
import pandas as pd 
import numpy as np
from src.exception import CustomException
from src.logger import logging
import dill
from sklearn.metrics import r2_score

from sklearn.model_selection import GridSearchCV
def evaluate_model(X_train, y_train, X_test, y_test, models,param):
    """
    This function evaluates the performance of a given model.
    
    Parameters:
    - X_train (DataFrame): Training features.
    - y_train (Series): Training target variable.
    - X_test (DataFrame): Testing features.
    - y_test (Series): Testing target variable.
    - model: The machine learning model to be evaluated.
    
    Returns:
    - r2_score_value (float): The R-squared score of the model.
    """
    try:
        report = {}
        for i in range(len(list(models))):
        
            model = list(models.values())[i]
            para= param[list(models.keys())[i]]

            print(f"Training model:", model)
            gs = GridSearchCV(model,para,cv=3)
            gs.fit(X_train,y_train)
            model.set_params(**gs.best_params_)
            model.fit(X_train, y_train)
            y_train_pred = model.predict(X_train)
            y_test_pred = model.predict(X_test)
            train_model_score = r2_score(y_train, y_train_pred)
            test_model_score = r2_score(y_test, y_test_pred)
            report[list(models.keys())[i]] = test_model_score
        return report

    except Exception as e:
        raise CustomException(e, sys) from e
    

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
    
def load_object(filepath):
    try:
        with open(filepath,'rb') as file_obj:
            return dill.load(file_obj)
    except Exception as e:
        raise CustomException(e, sys) 