import os
import sys
import numpy as np
import pandas as pd
import dill
from src.exception import CustomException
from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV


def save_object(file_path, obj):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file_obj:
            dill.dump(obj=obj, file=file_obj)
    
    
    except Exception as e:
        raise CustomException(e,sys)
    
def evaluate_model(xtrn,ytrn,xtst,ytst,models, params):
    try:
        report = {}

        for i in range(len(list(models))):
            model = list(models.values())[i]
            
            para = params[list(models.keys())[i]]

            # fitting on gridsearch to get best param
            GS_tuning = GridSearchCV(model, param_grid=para, cv=5)
            GS_tuning.fit(xtrn, ytrn)

            # fitting the model with best params
            best_parameters = GS_tuning.best_params_
            model.set_params(**best_parameters)
            model.fit(xtrn, ytrn)

            # prediction for both train and test
            ytrn_pred = model.predict(xtrn)
            ytst_pred = model.predict(xtst)

            # accuracy check
            trn_model_score = r2_score(ytrn, ytrn_pred)
            tst_model_score = r2_score(ytst, ytst_pred)

            report[list(models.keys())[i]] = tst_model_score

        return report, best_parameters

    except Exception as e:
        raise CustomException(e,sys)