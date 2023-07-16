import os
import sys
import pandas as pd
from src.logger import logging
from src.exception import CustomException

from sklearn.model_selection import train_test_split
from dataclasses import dataclass

from src.component.data_transformation import DataTransformation
from src.component.data_transformation import DataTransformationConfig

from src.component.model_trainer import ModelTrainer
from src.component.model_trainer import ModelTrainerConfig

@dataclass
class DataIngestionConfig:
    train_data_path : str=os.path.join('artifacts',"train.csv")
    test_data_path : str=os.path.join('artifacts',"test.csv")
    raw_data_path : str=os.path.join('artifacts',"raw.csv")

class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        logging.info('Entered into data ingestion component')
        try:
            # df = pd.read_csv("end to end ML/notebook/stud.csv")
            df = pd.read_csv("C:/Users/chand/OneDrive/Documents/AIML/end to end ML/notebook/stud.csv")
            logging.info("Successflly fetched dataset")
            
            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path), exist_ok=True)

            df.to_csv(self.ingestion_config.raw_data_path, index=False, header=True)

            logging.info('initiated train test split component')

            trn_dt, tst_dt = train_test_split(df, test_size=0.2, random_state=2)
            trn_dt.to_csv(self.ingestion_config.train_data_path, index=False, header=True)
            tst_dt.to_csv(self.ingestion_config.test_data_path,  index=False, header=True)

            logging.info('ingestion of data is completed')

            return(
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )
        except Exception as e:
            raise CustomException(e,sys)

#main function
if __name__=="__main__":
    obj = DataIngestion()
    train_data_path, test_data_path = obj.initiate_data_ingestion()

    data_transformation  = DataTransformation()
    train_arr, test_arr, _ = data_transformation.initiate_data_transformer(train_data_path, test_data_path)

    model_trainer = ModelTrainer()
    res, m = model_trainer.initiate_model_trainer(train_arr, test_arr)
    print("Accuracy  : ",res)
    print("Best Model: ",m)
