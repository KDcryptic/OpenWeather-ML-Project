import os
import sys
import pickle
import boto3

from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from catboost import CatBoostRegressor
from xgboost import XGBRegressor
import dill
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import(
    AdaBoostRegressor,
    GradientBoostingRegressor,
    RandomForestRegressor
)

from dataclasses import dataclass
from src.exception import CustomException
from src.logger import logging
from src.utils import downloadFiles, upload_to_s3, evaluate_model
from io import BytesIO

s3 = boto3.client('s3')
bucketName = 'open-weather-data-storage'
buffer = BytesIO()


@dataclass

class ModelTrainerConfig:

    trained_model_file_path= upload_to_s3(buffer,'models/trained','model.pkl',bucketName)


class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()

    def startTraining(self,train_arr,test_arr):

        try:

            logging.info("Splitting into train and test data")

            X_train, y_train, X_test,y_test=(

                train_arr[:,:-1],
                train_arr[:,-1],
                test_arr[:,:-1],
                test_arr[:,-1]
            )
            
            models = {

                'LinearRegression':LinearRegression(),
                'KNRegressor':KNeighborsRegressor(),
                'DecisionTreeRegressor':DecisionTreeRegressor(),
                'AdaBoostRegressor':AdaBoostRegressor(),
                'RandomForestRegressor':RandomForestRegressor(),
                'GradientBoostingRegressor':GradientBoostingRegressor()

            }

            model_report:dict=evaluate_model(X_train,y_train,X_test,y_test,models)

            best_model_score = sorted(max(model_report.values()))
            best_model_name = list(model_report.keys())[

                list(model_report.values()).index(best_model_score)
            ]

            best_model = models[best_model_name]

            if best_model_score < 0.6:
                raise CustomException('No good model found')
            logging.info('Best model on both training and data')

            dill.dump(best_model,buffer)


            upload_to_s3(buffer,'machineLearning/models','model.pkl',bucketName)

        except Exception as e:
            raise CustomException(e,sys)