#get the data, split etcm
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from src.logger import logging
from src.exception import CustomException
import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass
from src.components.data_transformation import DataTransformationConfig
from src.components.data_transformation import DataTransformation


@dataclass
class data_ingestion_config:
    """
    Configuration for data ingestion.
    """
    train_data_path: str = os.path.join("artifacts", "train.csv")
    test_data_path: str = os.path.join("artifacts", "test.csv")
    raw_data_path: str = os.path.join("artifacts", "raw.csv")

class DataIngestion:
    def __init__(self):
        self.ingestion_config = data_ingestion_config()
    def initiate_data_ingestion(self):
        """
        This function is used to initiate the data ingestion process.
        It reads the data from a CSV file, splits it into training and testing sets,
        and saves them to specified paths.
        """
        logging.info("Data Ingestion started")
        try:
            # Read the data from the CSV file
            df = pd.read_csv('notebook\data\stud.csv')
            logging.info("Data read successfully")

            # Create directories if they do not exist
            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path), exist_ok=True)

            # Save the raw data
            df.to_csv(self.ingestion_config.raw_data_path, index=False, header=True)
            logging.info("Raw data saved")
            logging.info("Train Test split initiated")
            # Split the data into training and testing sets
            train_set, test_set = train_test_split(df, test_size=0.2, random_state=42)

            # Save the training and testing sets
            train_set.to_csv(self.ingestion_config.train_data_path, index=False,header=True)
            test_set.to_csv(self.ingestion_config.test_data_path, index=False,header=True)

            logging.info("Data Ingestion completed successfully")
            return{
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path,
            }

        except Exception as e:
            raise CustomException(e, sys)
        
if __name__ == "__main__":
    obj = DataIngestion()
    train_data, test_data = obj.initiate_data_ingestion()
    data_transformation = DataTransformation()
    data_transformation.initiate_data_transformation(train_data, test_data)
    
