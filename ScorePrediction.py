import cv2
import mahotas
import numpy as np
from joblib import dump, load


clf = load("ModelRF.joblib")
bins             = 8

# feature-descriptor-1: Hu Moments
def fd_hu_moments(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    feature = cv2.HuMoments(cv2.moments(image)).flatten()
    return feature

# feature-descriptor-2: Haralick Texture
def fd_haralick(image):
    # convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # compute the haralick texture feature vector
    haralick = mahotas.features.haralick(gray).mean(axis=0)
    # return the result
    return haralick

# feature-descriptor-3: Color Histogram
def fd_histogram(image, mask=None):
    # convert the image to HSV color-space
    image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # compute the color histogram
    hist  = cv2.calcHist([image], [0, 1, 2], None, [bins, bins, bins], [0, 256, 0, 256, 0, 256])
    # normalize the histogram
    cv2.normalize(hist, hist)
    # return the histogram
    return hist.flatten()

def getScore(images):
    imageCount = 0
    total = 0
    for image in images:
        imageCount += 1
        # image = cv2.imread(file)

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

        # predict label of test image
        prediction = clf.predict(global_feature.reshape(1,-1))[0]
        prediction_proba = clf.predict_proba(global_feature.reshape(1,-1))[0]
        labels = [x for x in np.arange(1.2, 5, 0.1)]
        prediction = labels[prediction]
        idx = 0
        for prediction_p in prediction_proba:
            cr = prediction_proba[idx] * labels[idx]
            total += cr
            idx+=1

        
        # print(train_labels[int(mid)])
        # #show predicted label on image
        # cv2.putText(image, train_labels[prediction], (20,30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0,255,255), 3)

        # # # display the output image
        # plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        # plt.show()
    return str(total / imageCount)
