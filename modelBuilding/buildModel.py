from re import VERBOSE
from glo import fd_haralick, fd_histogram, fd_hu_moments
import h5py
import numpy as np
import os
import glob
from joblib import dump, load
import cv2
import warnings
from matplotlib import pyplot
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.model_selection import KFold, StratifiedKFold
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC

warnings.filterwarnings('ignore')

if not os.path.exists('./output'):
    os.makedirs('./output')
if not os.path.exists('./screens5000plus'):
    os.makedirs('./screens5000plus')



#--------------------
# tunable-parameters
#--------------------
num_trees = 100
test_size = 0.03
seed      = 9
train_path = "screens5000plus"
test_path  = "tests"
h5_data    = 'output/data.h5'
h5_labels  = 'output/labels.h5'
scoring    = "accuracy"

# # get the training labels
train_labels = os.listdir("./screens5000plus")

# # sort the training labels
train_labels.sort()


# import the feature vector and trained labels
h5f_data  = h5py.File(h5_data, 'r')
h5f_label = h5py.File(h5_labels, 'r')

global_features_string = h5f_data['dataset_1']
global_labels_string   = h5f_label['dataset_1']

global_features = np.array(global_features_string)
global_labels   = np.array(global_labels_string)

h5f_data.close()
h5f_label.close()


# verify the shape of the feature vector and labels
print("[STATUS] features shape: {}".format(global_features.shape))
print("[STATUS] labels shape: {}".format(global_labels.shape))

print("[STATUS] training started...")

# split the training and testing data
(trainDataGlobal, testDataGlobal, trainLabelsGlobal, testLabelsGlobal) = train_test_split(np.array(global_features),
                                                                                          np.array(global_labels),
                                                                                          test_size=test_size,
                                                                                          random_state=seed)

print("[STATUS] splitted train and test data...")
print("Train data  : {}".format(trainDataGlobal.shape))
print("Test data   : {}".format(testDataGlobal.shape))
print("Train labels: {}".format(trainLabelsGlobal.shape))
print("Test labels : {}".format(testLabelsGlobal.shape))

#-----------------------------------
# TESTING OUR MODEL
#-----------------------------------

# to visualize results
import matplotlib.pyplot as plt

# create the model - Random Forests
clf  = RandomForestClassifier(n_estimators=num_trees, random_state=seed, verbose = 1)

# fit the training data to the model
clf.fit(trainDataGlobal, trainLabelsGlobal)

clf = dump(clf, 'ModelRF.joblib') 

# loop through the test images
for file in glob.glob(test_path + "/*.png"):
    # read the image
    image = cv2.imread(file)

    # resize the image

    ####################################
    # Global Feature extraction
    ####################################
    fv_hu_moments = fd_hu_moments(image)
    fv_haralick   = fd_haralick(image)
    fv_histogram  = fd_histogram(image)

    ###################################
    # Concatenate global features
    ###################################
    global_feature = np.hstack([fv_histogram, fv_haralick, fv_hu_moments])

    # scale features in the range (0-1)

    # predict label of test image
    prediction = clf.predict(global_feature.reshape(1,-1))[0]
    prediction_proba = clf.predict_proba(global_feature.reshape(1,-1))[0]

    fRes = 0
    idx = 0
    mid = len(prediction_proba) / 2
    for f in train_labels:
        # fRes += float(train_labels[idx]) * prediction_proba[idx]
        if prediction_proba[idx] > 0.01 and idx > mid:
            mid += 1
        if "4" in train_labels[int(mid)]:
            fRes += (float(train_labels[idx]) / 2) * prediction_proba[idx]
        else:
            fRes += float(train_labels[idx]) * prediction_proba[idx]


        idx += 1

    print(fRes)
    print(prediction_proba)
    print(train_labels[int(mid)])
    #show predicted label on image
    cv2.putText(image, train_labels[prediction], (20,30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0,255,255), 3)

    # # display the output image
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.show()