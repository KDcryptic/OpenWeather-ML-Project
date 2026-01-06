import sys
import os
from datetime import datetime
import logging

FILE_Name = f'{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log'
log_path = os.path.join(os.getcwd(),'logs',FILE_Name)
os.makedirs(log_path,exist_ok=True)

log_filepath = os.path.join(log_path,FILE_Name)

logging.basicConfig(

    filename=log_filepath,
    format= "[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
    
)