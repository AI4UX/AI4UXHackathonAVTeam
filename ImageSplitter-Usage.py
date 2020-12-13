
from ImageSplitter import returnSplitAppImagesOfAllApps
from ImageSplitter import returnSplitImagesOfApp
import cv2
import time

def UseReturnSplitAppImagesOfAllApps():
    allAppImageData = returnSplitAppImagesOfAllApps()

    print('returnSplitAppImagesOfAllApps()')
    for appData in allAppImageData: # allAppImageData (dict)
            for imgData in allAppImageData[appData]: # allAppImageData[appId] (array)
                print('\n appId ' + appData)

                for viewIndex in imgData: # thisAppImgData (array)
                
                    for viewArr in viewIndex:
                        fullArr = viewIndex[viewArr]

                        print('\n' + viewArr)
                        index = 0
                        for croppedImg in fullArr:
                            #croppedImg = viewIndex[viewArr]
                            print('index ' + str(index))
                            cv2.destroyAllWindows()
                            cv2.imshow('croppedImg', croppedImg) 
                            cv2.waitKey(1)
                            time.sleep(0.5)  
                            index += 1


def UseReturnSplitImagesOfApp(appId):
    singleAppImageData = returnSplitImagesOfApp(appId)

    print('returnSplitImagesOfApp()')
    print(appId)
    for a in singleAppImageData:
        #print('\na ')
        #print(a)
        for b in singleAppImageData[a]:
            #print('\nb')
            #print(b)
            for c in singleAppImageData[a][b]:
                #print('\nc')
                #print(c)
                for d in c:
                    #print('\nd')
                    #print(c[d])
                    print('\n' + d)
                    index = 0
                    for e in range(len(c[d])):
                        croppedImg = c[d][e]
                        print('index ' + str(index))
                        cv2.destroyAllWindows()
                        cv2.imshow('croppedImg', croppedImg) 
                        cv2.waitKey(1)
                        time.sleep(0.5)  
                        index += 1
        
                        

# appId = 'air.com.eprize.nylottery.app.NYLotteryApp'
# UseReturnSplitImagesOfApp(appId)

#UseReturnSplitAppImagesOfAllApps()

     

