# TB-prediction

In this experiment, we evaluated a hybrid model; this model has a deep learning feature extractor coupled to a machine learning classifier.
Feature extraction using pretrained VGG16 network and integrating a  XGBoost classifier for classification. 

Requirements

* numpy 
* matplotlib
* glob
* cv2
* xgboost
* keras
* os
* mlxtend
* Python 3.7 or higher 
* Kaggle Dataset https://www.kaggle.com/datasets/tawsifurrahman/tuberculosis-tb-chest-xray-dataset


Process
* Once the dataset is downloaded, extract the images contained in the Kaggle compressed folder to the environment to be used for the simulation.
* Load the relevant Jupyter Notebooks in the Python environment to be used for the simulation.
* Amend the lines of code referencing the location \ path to the extracted Kaggle data.
* Run the code


Motivation of the study:

1. The prevalence of Tuberculosis:
* Globally TB kills more people than any other single infectious disease.
* According to the WHO, the number of TB deaths increase annually 
2. And the scarcity of resources to tackle it:
* This is due to slow diagnostics methods and scarcity of radiologists. 
* Chest radiography screening is commonly used because of its cost effectiveness and mass deployment capabilities. 
* TB diagnosis in some regions is still a difficult task

To address this issue computer aided detection (CAD) systems are developed to automatically detect TB from chest x-ray.
