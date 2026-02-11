from setuptools import setup,find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name= "ECOMMERCE PRODUCT RECOMMENDER",
    version= "0.3",
    author= "sambit",
    packages= find_packages(),
    install_requires= requirements 
)