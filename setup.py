from setuptools import setup, find_packages
from typing import List

HYPHEN_E_DOT ='-e .'

def get_requirement(file:str)->List:
    requirements = []
    with open(file) as file_obj:
        requirements = file_obj.readlines()
        requirements = [requirement.replace('\n','') for requirement in requirements]

        if HYPHEN_E_DOT in requirements:
            requirements.remove(HYPHEN_E_DOT)
    return requirements

setup(
    name='Diamond Price Prediction',
    version='0.0.1',
    author='Ravi', 
    author_email="raviiai@gmail.com",
    install_requires=get_requirement('requirements.txt'),
    packages=find_packages()
)