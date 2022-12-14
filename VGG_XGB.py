# Import libraries

import os
import numpy as np 
import matplotlib.pyplot as plt
import glob
import cv2
import xgboost as xgb
from sklearn import preprocessing
from keras.models import Model, Sequential
from keras.layers import Dense, Flatten, Conv2D, MaxPooling2D
from sklearn import metrics
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report
from mlxtend.plotting import plot_confusion_matrix
from keras.applications.vgg16 import VGG16


# Read input images 
print(os.listdir("path to where your images are"))

#Capture training data and labels into respective lists
train_images = []
train_labels = [] 

SIZE = 150

for directory_path in glob.glob("path"):
    label = directory_path.split("\\")[-1]
    for img_path in glob.glob(os.path.join(directory_path, "*.png")):
        img = cv2.imread(img_path, cv2.IMREAD_COLOR)       
        img = cv2.resize(img, (SIZE, SIZE))
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        train_images.append(img)
        train_labels.append(label)
        
#Convert lists to arrays        
train_images = np.array(train_images)
train_labels = np.array(train_labels)   


# Capture test data and labels into respective lists

test_images = []
test_labels = [] 
for directory_path in glob.glob("path"):
    fruit_label = directory_path.split("\\")[-1]
    for img_path in glob.glob(os.path.join(directory_path, "*.png")):
        img = cv2.imread(img_path, cv2.IMREAD_COLOR)
        img = cv2.resize(img, (SIZE, SIZE))
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        test_images.append(img)
        test_labels.append(fruit_label)

#Convert lists to arrays                
test_images = np.array(test_images)
test_labels = np.array(test_labels)

#Encode labels from text to integers.

le = preprocessing.LabelEncoder()
le.fit(train_labels)
train_labels_encoded = le.transform(train_labels)
le.fit(test_labels)
test_labels_encoded = le.transform(test_labels)

#Split data into test and train datasets (already split but assigning to meaningful convention)
x_train, y_train, x_test, y_test = train_images, train_labels_encoded, test_images, test_labels_encoded

# Normalize pixel values to between 0 and 1
x_train, x_test = x_train / 255.0, x_test / 255.0

#Load model wothout classifier/fully connected layers
VGG_model = VGG16(weights='imagenet', include_top=False, input_shape=(SIZE, SIZE, 3))

#Make loaded layers as non-trainable. This is important as we want to work with pre-trained weights
for layer in VGG_model.layers:
    layer.trainable = False
    
VGG_model.summary()  #Trainable parameters will be 0

#Now, extract the draining data features with the CNN 
feature_extractor=VGG_model.predict(x_train)

#Flatten the features
features = feature_extractor.reshape(feature_extractor.shape[0], -1)
X_for_training = features #This is our X input to XGB

#Train XGB classifier using the training dataset features
model = xgb.XGBClassifier(use_label_encoder=False,eval_metric='logloss')
model.fit(X_for_training, y_train) 

#Send test data through same feature extractor process
X_test_feature = VGG_model.predict(x_test)
X_test_features = X_test_feature.reshape(X_test_feature.shape[0], -1)

#Now predict using the trained XGB model. 
prediction = model.predict(X_test_features)
#Inverse le transform to get original label back. 
prediction = le.inverse_transform(prediction)

#Plot a confusion matrix
cm= confusion_matrix(test_labels, prediction)
plot_confusion_matrix(cm, figsize=(5,5));

#Print overall accuracy
print ("Accuracy = ", metrics.accuracy_score(test_labels, prediction))
print(classification_report(test_labels, prediction))   

#Check results on a few select images
n=np.random.randint(0, x_test.shape[0])
img = x_test[n]
plt.imshow(img)
input_img = np.expand_dims(img, axis=0) #Expand dims so the input is (num images, x, y, c)
input_img_feature=VGG_model.predict(input_img)
input_img_features=input_img_feature.reshape(input_img_feature.shape[0], -1)
prediction = model.predict(input_img_features)[0] 
prediction = le.inverse_transform([prediction])  #Reverse the label encoder to original name
print("The prediction for this image is: ", prediction)
print("The actual label for this image is: ", test_labels[n])

