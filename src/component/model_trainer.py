import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import sys

# modeling module
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import AdaBoostRegressor, RandomForestRegressor
from sklearn.svm import SVR
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.model_selection import RandomizedSearchCV
from sklearn.model_selection import train_test_split

from catboost import CatBoostRegressor
from xgboost import XGBRegressor
import warnings
warnings.filterwarnings("ignore")

from src.exception import CustomException
from src.logger import logging
from src.utils import save_object, evaluate_model
from dataclasses import dataclass


@dataclass
class ModelTrainerConfig:
    model_train_path = os.path.join('artifacts', 'model.pkl')

class ModelTrainer:
    def __init__(self):
        self.get_train_model_path = ModelTrainerConfig()

    def initiate_model_trainer(self, train_arr, test_arr):
        try:
            logging.info("Fetching data and spliting into train test")
            x_train, x_test, y_train, y_test = (
                train_arr[:, :-1],
                test_arr[:, :-1],
                train_arr[:, -1],
                test_arr[:, -1]
            )

            models = {
                "Linear Regression":LinearRegression(),
                "KN Regressor":KNeighborsRegressor(),
                "Decision Tree":DecisionTreeRegressor(),
                "Ramdom Forest":RandomForestRegressor(),
                "XGBoost Regressor":XGBRegressor(),
                "CatBoost Regressor":CatBoostRegressor(verbose=False),
                "AdaBoost Regressor":AdaBoostRegressor()
            }

            # hyperparameter tuning
            params = {
                "Linear Regression":{
                    
                },
                "Gradient Boosting":{
                    'n_estimators':[16,32,64,128,256],
                    'learning_rate':[0.01,0.05,0.1],
                    'subsample':[0.6, 0.7, 0.8, 0.9]
                },
                "KN Regressor":{
                    'n_neighbors':[5,7,9,11]
                },
                "Decision Tree":{
                    'criterion':['squared_error', 'friedman_mse', 'absolute_error', 'poisson'],
                    'max_features':['sqrt', 'log2']

                },
                "Ramdom Forest":{
                    'n_estimators':[16,32,64,128,256]   

                },
                "XGBoost Regressor":{
                    'learning_rate':[0.01, 0.05,0.1,0.001],
                    'n_estimators':[16,32,64,128,256]
                },
                "CatBoost Regressor":{
                    'depth':[6,8,10],
                    'learning_rate':[0.01,0.05,0.1],
                    'iterations':[30,50,100]
                },
                "AdaBoost Regressor":{
                    'learning_rate':[0.001, 0.01, 0.1, 0.5],
                    'loss':['linear', 'square', 'exponential'],
                    'n_estimators':[16,32,64,128,256]
                }
            }

            # creating models
            model_report, best_parameters = evaluate_model(xtrn=x_train, ytrn=y_train, xtst=x_test, ytst=y_test, models=models, params=params)
            
            # to get best model score from report
            all_models = sorted(model_report.values())
            best_model_score = max(all_models)

            # to get best model name from report
            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]

            # model object
            best_model = models[best_model_name]

            if best_model_score < 0.7:
                logging.info("All models estimates its accuracy under 70%")
                raise CustomException("No best model found")

            logging.info("Successfully found the best model - ")
            # logging.info("Successfully found the best model - ",best_model) 
            # when i keep it like this, this gets printed in the terminal instead of storing into logs

            save_object(
                file_path=ModelTrainerConfig.model_train_path,
                obj=best_model
            )

            # predicted model
            predicted = best_model.predict(x_test)
            r2 = r2_score(y_true=y_test, y_pred=predicted)
            return r2, best_model, best_parameters

        except Exception as e:
            raise CustomException(e,sys)






