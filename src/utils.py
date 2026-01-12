import boto3
import sys
import pandas as pd
import numpy as np
from src.logger import logging
from src.exception import CustomException
from io import BytesIO

def upload_to_s3(dataPath,folder,fileName,bucketName):

    try:

        key=f'{folder}/{fileName}'
        s3.put_object(
        Bucket=bucketName,
        Key=key,
        Body=dataPath.getvalue(),
        ContentType="text/csv"
    )
        logging.info(f"Uploaded {key} to {bucketName}")

    except Exception as e:
        raise CustomException(e,sys)


def downloadFiles(csv_buffer,fileName):
    
    try:
        
        
        s3.download_fileobj(bucketName, f'{fileName}', csv_buffer)
        logging.info('File Downloaded!')
        csv_buffer = BytesIO(csv_buffer.getvalue())
        df = pd.read_csv(csv_buffer)

        return df
        
        
    except Exception as e:
        raise CustomException(e,sys)
    
    def evaluate_model(X_train,y_train,X_test,y_test, models):

        try:

            report = {}

            for i in range(len(list(models))):

                model = list(models.values())[i]

                model.fit(X_train,y_train)

                y_train_predict=model.predict(X_train)

                y_test_predict=model.predict(y_test)

                train_model_score = r2_score(y_train,y_train_predict)
                test_model_score = r2_score(y_test,y_test_predict)

                report[list(models.keys())[i]]=test_model_score

            return report


        except Exception as e:
            raise CustomException(e,sys)