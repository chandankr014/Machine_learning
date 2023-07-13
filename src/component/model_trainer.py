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
                "Lasso":Lasso(),
                "Ridge":Ridge(),
                "KN Regressor":KNeighborsRegressor(),
                "Decision Tree":DecisionTreeRegressor(),
                "Ramdom Forest":RandomForestRegressor(),
                "XGBoost Regressor":XGBRegressor(),
                "CatBoost Regressor":CatBoostRegressor(verbose=False),
                "AdaBoost Regressor":AdaBoostRegressor()
            }
            model_report:dict = evaluate_model(xtrn=x_train, ytrn=y_train, xtst=x_test, ytst=y_test, models=models)

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

            logging.info("Successfully found the best model")

            save_object(
                file_path=ModelTrainerConfig.model_train_path,
                obj=best_model
            )

            # predicted model
            predicted = best_model.predict(x_test)
            r2 = r2_score(y_true=y_test, y_pred=predicted)
            return r2

        except Exception as e:
            raise CustomException(e,sys)






