import os
import sys
import numpy as np
import pandas as pd
import dill
from src.exception import CustomException
from sklearn.metrics import r2_score


def save_object(file_path, obj):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file_obj:
            dill.dump(obj=obj, file=file_obj)
    
    
    except Exception as e:
        raise CustomException(e,sys)
    
def evaluate_model(xtrn,ytrn,xtst,ytst,models):
    try:
        report = {}

        for i in range(len(list(models))):
            model = list(models.values())[i]
            model.fit(xtrn, ytrn)

            ytrn_pred = model.predict(xtrn)
            ytst_pred = model.predict(xtst)

            trn_model_score = r2_score(ytrn, ytrn_pred)
            tst_model_score = r2_score(ytst, ytst_pred)

            report[list(models.keys())[i]] = tst_model_score

        return report

    except Exception as e:
        raise CustomException(e,sys)