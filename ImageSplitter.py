
import os
import cv2
import time
import numpy as np
import pandas as pd
from pathlib import Path

# - - - - - - - - - - - - - - 

imageDirectory = 'uploads'

imgViewSets = [
                [1, 5], 
                [4, 4], # [horizontalPartitions, verticalPartitions]
                [5, 5], 
                [5, 1]
                ]

# - - - - - - - - - - - - - - 


df = pd.read_csv('newDf.csv')
records = df.to_dict(orient='dict')
records = df.set_index('App Id').T

def getSplitImages(imgPath, allAppImageData):
    filename = os.path.basename(imgPath)
    full_size_img = cv2.imread(imgPath)

    numEnd = filename.find('.png')
    appId = filename[0:numEnd-1]
    thisAppImgData = {}

    def showOriginalImg():
        cv2.destroyAllWindows()
        cv2.imshow('full_size_img', full_size_img) 
        cv2.waitKey(1)
        #time.sleep(1)

        cv2.destroyAllWindows()
        #time.sleep(0.5)

    def evaluateViews():

        viewSetNum = 0
        for viewSet in imgViewSets:
            viewSetNum = viewSetNum + 1

            viewDataToSave = {} # thisAppImgData: key = view#, value = viewDataToSave (array)

            btnsInCurView = 0

            horizPartitions = viewSet[0]
            vertPartitions = viewSet[1]

            origHeight, origWidth, channels = full_size_img.shape
            cropWidth = int(origWidth/horizPartitions)
            cropHeight = int(origHeight/vertPartitions)

            print('\n'+filename)
            print('image height, width = ' + str(cropWidth) + ', ' + str(cropHeight))

            for x in range(horizPartitions):
                curViewSet = [] # will contain cropped images, not stored in dictionary
                imageNum = filename[numEnd-1:numEnd]

                for y in range(vertPartitions):
                    cropStartX = cropWidth * (x)
                    cropStartY = cropHeight * (y)
                    cropEndX = cropWidth * (x+1)
                    cropEndY = cropHeight * (y+1)

                    # this actually crops the image
                    crop_img = full_size_img[cropStartY:cropEndY, cropStartX:cropEndX].copy()
                    print("\nview " + str(y+1))
                    print("x " + str(cropStartX) + ' ' + str(cropEndX))
                    print("y " + str(cropStartY) + ' ' + str(cropEndY))

                    print('end of view reached\n')
                    #viewDataToSave['view'+str(y+1)] = {}
                    #viewDataToSave['view'+str(y+1)]['rects'] = 2 # test

                    curViewSet.append(crop_img)

                    #if len(curViewSet) > 0:
                        #cv2.destroyAllWindows()
                        #cv2.imshow('cropped_img', curViewSet[len(curViewSet)-1]) 
                        #cv2.waitKey(1)
                        #time.sleep(0.5)                                
                            
                # btnsInCurView = 2 # test
                # viewDataToSave['view'+str(y)] = {}
                # viewDataToSave['view'+str(viewSetNum)] = {}
                # viewDataToSave['view'+str(viewSetNum)]['btns'] = btnsInCurView # test

                thisAppImgData['img'+str(imageNum)] = curViewSet # viewDataToSave
                #print('curViewSet')
                #print(curViewSet)
                    
        print(appId)
        if allAppImageData.get(appId) == None:
            allAppImageData[appId] = []

        allAppImageData[appId].append(thisAppImgData)
        
    #showOriginalImg()
    evaluateViews()

    #print('allAppImageData[appId]')
    #print(allAppImageData[appId])
    return allAppImageData
    


def returnSplitImagesOfApp(appId, sentDir):

    thisAppImgData = {}

    for filename in os.listdir(sentDir):
        if filename.endswith(".png") or filename.endswith(".jpg") or filename.endswith(".jpeg"):
            if filename.startswith(appId):
                fileType = Path(filename).suffix
                numEnd = filename.find(fileType)
                imageNum = filename[numEnd-1:numEnd]
                imgPath = sentDir + '/' + filename
                returnedVal = getSplitImages(imgPath, {})
                print('returned val of returnSplitImagesOfApp')
                print(returnedVal)
                thisAppImgData['img'+str(imageNum)] = returnedVal

    return(thisAppImgData)



def returnSplitAppImagesOfAllApps():
    
    allAppImageData = {}
    appCount = 0
    directoryToUse = None

    if dir == None:
        directoryToUse = imageDirectory
    else:
        directoryToUse = dir

    for filename in os.listdir(directoryToUse):

        if filename.endswith(".png"):
            if True: #appCount < 10

                thisAppImgData = {} # will store the data of each view of the single app image

                numEnd = filename.find('.png')
                appId = filename[0:numEnd-1]
                imageNum = filename[numEnd-1:numEnd]
                
                print('\nappId: ' + appId)
                print('rating: ' + str(records[appId]['Rating']))
                        
                imgPath = imageDirectory + '/' + filename
                returnedVal = getSplitImages(imgPath, thisAppImgData)
                print('returned val of getSplitImages')
                for k in returnedVal:
                    newArr = returnedVal[k]

                    if allAppImageData.get(k) == None:
                        allAppImageData[k] = []

                    allAppImageData[k].append(newArr)
                    
                continue

        appCount = appCount + 1

    return allAppImageData



