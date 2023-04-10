import sys
import os
from src.exception_handling import CustomException
from src.logger import logging
import pickle



def save_object(file_path, obj):
    try:
        dir_path = os.path.dirname(file_path)

        os.makedirs(dir_path, exist_ok=True)

        with open(file_path, 'wb') as file_obj:
            pickle.dump(obj, file_obj)
    except Exception as e:
        logging.info("error while saving preprocessor object in utils.py file")
        raise CustomException(e, sys)