import os
import sys
import pandas as pd
from src.logger import logging
from src.exception import CustomException

from sklearn.model_selection import train_test_split
from dataclasses import dataclass

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
            df = pd.read_csv("end to end ML/notebook/stud.csv")
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
    obj.initiate_data_ingestion()
