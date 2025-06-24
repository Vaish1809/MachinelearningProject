#process the data for the model
import os
import sys  
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from dataclasses import dataclass
import pandas as pd
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder 
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from src.logger import logging
from src.exception import CustomException
from src.utils import save_object





@dataclass
class DataTransformationConfig:
    """
    Configuration for data transformation.
    to save model in pickle file
    """
    preprocessor_obj_file_path = os.path.join("artifacts", "preprocessor.pkl")

class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    def get_data_transformer_object(self):
        """
        This function creates a data transformation pipeline.
        It handles numerical and categorical features separately.
        """
        try:
            numerical_columns = ['writing_score', 'reading_score']
            categorical_columns =["gender","race_ethnicity", "parental_level_of_education", "lunch", "test_preparation_course"]

            # Numerical pipeline
            numerical_pipeline = Pipeline(
                steps=[
                ('imputer', SimpleImputer(strategy='mean')),
                ('scaler', StandardScaler())
            ]
            )
            logging.info("Numerical pipelines created successfully")
            # Categorical pipeline
            categorical_pipeline = Pipeline(
                steps=[
                ('imputer', SimpleImputer(strategy='most_frequent')),
                ('onehotencoder', OneHotEncoder()),
                ('scaler', StandardScaler(with_mean=False))  # Set with_mean=False to avoid issues with sparse matrices
            ]
            )
            logging.info("Categorical pipelines created successfully")
            # Combine both pipelines into a preprocessor
            preprocessor = ColumnTransformer(
             [
                    ('numerical_pipeline', numerical_pipeline, numerical_columns),
                    ('categorical_pipeline', categorical_pipeline, categorical_columns)
                ]
            )
            return preprocessor
        
        except Exception as e:
            raise CustomException(e, sys)
        
    def initiate_data_transformation(self, train_path, test_path):
            try:
                train_df = pd.read_csv(train_path)
                test_df = pd.read_csv(test_path)    


                logging.info("Train and test data read successfully for transformation")

                logging.info("Obtaining preprocessing object")

                preprocessor_obj = self.get_data_transformer_object()

                target_column_name = 'math_score'
                numerical_columns = ['writing_score', 'reading_score']

                #Xtrain
                input_feature_train_df = train_df.drop(columns=[target_column_name], axis=1)
                #Ytrain
                target_feature_train_df = train_df[target_column_name]
                #Xtest
                input_feature_test_df = test_df.drop(columns=[target_column_name], axis=1)
                #ytest
                target_feature_test_df = test_df[target_column_name]
                
                logging.info("Applying preprocessing object on training and testing dataframes")

                # Transform the input features
                input_feature_train_arr = preprocessor_obj.fit_transform(input_feature_train_df)    
                input_feature_test_arr = preprocessor_obj.transform(input_feature_test_df)
                train_arr = np.c_[
                    input_feature_train_arr,np.array(target_feature_train_df)
                ]
                test_arr = np.c_[
                    input_feature_test_arr, np.array(target_feature_test_df)
                ]
                logging.info("Saved preprocessor object")

                save_object(
                    file_path = self.data_transformation_config.preprocessor_obj_file_path,
                    obj = preprocessor_obj
                )
                return(
                    train_arr,
                    test_arr,
                    self.data_transformation_config.preprocessor_obj_file_path,   

                )

              
            except Exception as e:
                raise CustomException(e, sys)
            