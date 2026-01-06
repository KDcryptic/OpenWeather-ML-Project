import pandas as pd
import numpy as np
import requests
import os
import json
import sys
import boto3

from datetime import datetime
from dataclasses import dataclass
from src.exception import CustomException
from src.logger import logging
from io import StringIO


openWeatherKey = os.getenv('openWeatherKey')
bucketName = 'open-weather-data-storage'
csv_buffer = StringIO()
s3 = boto3.client('s3')
base_url = "http://api.openweathermap.org/data/2.5/weather?"



namibia_settlements = [
    
    "Windhoek",
    "Swakopmund", "Walvis Bay", "Arandis", "Usakos", "Omaruru", "Henties Bay",
    "Oshakati", "Ongwediva", "Ompundja",
    "Eenhana", "Helao Nafidi",
    "Tsandi", "Okahao",
    "Tsumeb", "Oniipa",
    "Otjiwarongo", "Grootfontein", "Okakarara",
    "Opuwo", "Khorixas",
    "Katima Mulilo", "Kongola",
    "Rundu", 'Otjiwarongo',
    "Mariental", "Rehoboth", "Gibeon",
    "Keetmanshoop", "Lüderitz", "Oranjemund", "Karasburg",
    "Gobabis", "Leonardville", "Witvlei"

]

def getSettlementData(settlement):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={settlement}&appid={openWeatherKey}&units=metric"
    response = requests.get(url)
    data = response.json()

   
    if data.get("cod") != 200:
        logging.warning(f"Settlement '{settlement}' not found. Error: {data.get('message')}")
        return None

    settlementData = {
        'city': settlement,
        "lat": data["coord"]["lat"],
        "lon": data["coord"]["lon"],
        "temp": data["main"]["temp"],
        "feels_like": data["main"]["feels_like"],
        "temp_min": data["main"]["temp_min"],
        "temp_max": data["main"]["temp_max"],
        "pressure": data["main"]["pressure"],
        "humidity": data["main"]["humidity"],
        "wind_speed": data["wind"]["speed"],
        "clouds": data["clouds"]["all"],
        "weather": data["weather"][0]["description"],
        "sunrise": data["sys"]["sunrise"],
        "sunset": data["sys"]["sunset"],
        "timestamp": data["dt"]
    }

    return pd.DataFrame([settlementData])




def compileData(dataframes):
    
    try:
        df = pd.concat(dataframes, ignore_index=True)
        logging.info('hourly dataset compiled')
        fileName = f'weatherData_{datetime.now().strftime("%d_%m_%Y_%H_%M_%S")}.csv'
        df.to_csv(csv_buffer, index=False)
        upload_to_s3(csv_buffer,'raw/hourlyDatasets',fileName)
        logging.info(f" Weather data saved to {'datalake'}")
    
    except Exception as e:
        raise CustomException(e,sys)



def upload_to_s3(dataPath,folder,fileName):

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



dataframes = []


try:
    for settlement in namibia_settlements:
        settlementDf = getSettlementData(settlement)
        if settlementDf is not None:   
            dataframes.append(settlementDf)
        else:
            logging.info(f" Skipped {settlement}")
    
    compileData(dataframes)
    logging.info('File uploaded to datalake')

except Exception as e:
    raise CustomException(e,sys)




