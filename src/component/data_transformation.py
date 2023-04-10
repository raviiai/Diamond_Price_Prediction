import os
from dataclasses import dataclass
import sys
from src.logger import logging
from src.exception_handling import CustomException
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OrdinalEncoder
from src.utils import save_object
import pandas as pd
import numpy as np
from sklearn.compose import ColumnTransformer

@dataclass
class DataTransformationConfig:
    data_transformation_path = os.path.join('artifacts','preprocessor.pkl')

class DataTransformation:
    def __init__(self):
        self.data_config_obj = DataTransformationConfig()

    def get_data_transformation_object(self):
        try:
            logging.info("Data transformation initiated")

            categorical_cols = ['cut', 'color', 'clarity']
            numerical_cols = ['carat', 'depth', 'table', 'x', 'y', 'z']
            # for ordinal ranking
            cut_categories = ['Good', 'Very Good', 'Fair', 'Premium', 'Ideal']
            color_categories = ['D', 'E', 'F', 'G', 'H', 'I', 'J']
            clarity_categories = ['I1','SI2','SI1','VS2','VS1','VVS2','VVS1','IF'] 
            
            logging.info("pipeling started")

            numerical_pipeline = Pipeline(
                steps = [
                    ('imputer', SimpleImputer(strategy='median')),
                    ('scaling', StandardScaler())
            ])

            categorical_pipeline = Pipeline(
                steps=[
                    ('imputer', SimpleImputer(strategy='most_frequent')),
                    ('encoder', OrdinalEncoder(categories=[cut_categories, color_categories, clarity_categories]))
                ])

            preprocessor = ColumnTransformer([
                ('num_pipeline', numerical_pipeline, numerical_cols),
                ('cat_pipeline', categorical_pipeline, categorical_cols)
            ])

            return preprocessor

        except Exception as e:
            logging.info("Error while getting data Transformation object")
            raise CustomException(e, sys)
    
    def initiate_data_transformation(self, train_path, test_path):
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path) 
            logging.info("train and test data read sucessful...")

            #getting preprocessing object
            preprocessing_obj = self.get_data_transformation_object()

            target_col = 'price'
            drop_col = [target_col, 'id']

            input_feature_train_df = train_df.drop(columns=drop_col)
            target_feature_train_df = test_df[target_col]

            input_feature_test_df = test_df.drop(columns=drop_col)
            target_feature_test_df = test_df[target_col]

            #transforming
            input_feature_train_arr=preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr=preprocessing_obj.transform(input_feature_test_df)

            logging.info("Applying preprocessing")


            train_arr = np.c_[input_feature_train_arr, np.array(input_feature_train_df)]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]

            save_object(
                file_path=self.data_config_obj.data_transformation_path,
                obj=preprocessing_obj
            )
        except Exception as e:
            logging.info("Error Occured at Data Transformation file")
            raise CustomException(e, sys)