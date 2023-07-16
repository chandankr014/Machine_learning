import os
import sys
from dataclasses import dataclass

import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.exception import CustomException
from src.logger import logging
from src.utils import save_object


@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path = os.path.join('artifacts', "preprocessor.pkl")

class DataTransformation():
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    def get_data_transformer(self):
        try:
            categorical_col = ['gender', 'race_ethnicity', 'parental_level_of_education', 'lunch', 'test_preparation_course']
            numerical_col = ['writing_score', 'reading_score']

            num_pipeline = Pipeline(
                steps=[
                    ('imputer', SimpleImputer(strategy='median')),
                    ('scaler', StandardScaler(with_mean=False))
                ]
            )
            cat_pipeline = Pipeline(
                steps=[
                    ('imputer', SimpleImputer(strategy='most_frequent')),
                    ('encoder', OneHotEncoder(handle_unknown='ignore')),
                    ('scaler', StandardScaler(with_mean=False))
                ]
            )
            # in num_pipeline imputing -> scaling 
            # in cat_pipeline imputing -> encoding -> scaling 

            # getting logs
            logging.info("Pipelining is being performed...")
            logging.info("Numerical features standard scaling completed")
            logging.info("Categorical features encoding completed")

            preprocessor = ColumnTransformer(
                [
                    ('num_pipeline', num_pipeline, numerical_col),
                    ('cat_pipeline', cat_pipeline, categorical_col)
                ]
            )

            return preprocessor

        except Exception as e:
            raise CustomException(e,sys)


    def initiate_data_transformer(self, trn_path, tst_path):
        try:
            trn = pd.read_csv(trn_path)
            tst = pd.read_csv(tst_path)
        
            logging.info('Read train and test data completed')
            logging.info('Obtaining preprocessor object')

            preprocessor_obj = self.get_data_transformer()
            target_column_name = 'math_score'
            numerical_columns = ['writing_score', 'reading_score']

            ip_features_trn = trn.drop(columns=[target_column_name], axis=1)
            target_feature_trn = trn[target_column_name]

            ip_features_tst = tst.drop(columns=[target_column_name], axis=1)
            target_feature_tst = tst[target_column_name]

            print(ip_features_trn.shape, ip_features_tst.shape)

            logging.info(
                f"Applying preprocessing object on training dataframe and testing dataframe"
            )

            ip_feature_train_model = preprocessor_obj.fit_transform(ip_features_trn)
            ip_feature_test_model = preprocessor_obj.transform(ip_features_tst)
        
            train_arr = np.c_[
                ip_feature_train_model, np.array(target_feature_trn)
            ]
            test_arr = np.c_[
                ip_feature_test_model, np.array(target_feature_tst)
            ]

            logging.info("Saved Preprocessign Object")

            save_object(
                file_path = self.data_transformation_config.preprocessor_obj_file_path,
                obj = preprocessor_obj
            )

            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path
            )

        except Exception as e:
            raise CustomException(e,sys)
