from os import path, system
import time
import urllib
from pandas.core.frame import DataFrame
from urllib import request
import scipy.misc
import imageio
import sys, os
import pathlib
import requests
from threading import Thread
import cv2
import numpy as np
from skimage.io import imread, imshow, imsave
import os
from skimage import filters
from sklearn import feature_extraction
from sklearn.neighbors import KNeighborsClassifier
import re
from sklearn.feature_extraction import image as ii
import pandas as pd

# api-endpoint 
class Scrapper:
    def __init__(self):
        super().__init__()
        self.count = 0
        self.forbidden = [
        "Action",
        "Adventure",
        "Arcade",
        "Strategy",
        "Board",
        "Casino",
        "Card",
        "Casual",
        "No other languages",
        "Comics",
        "Entertainement",
        "Maps & Navigation",
        "Racing",
        "Role Playing",
        "Simulation",
        "Strategy",
        "Puzzle",
        "Personalization",
        "Trivia",
        "Word",
        ]
        self.appCountLimit = 3
        self.yearLimit = 2017
        self.limitLess = 100000
        self.limitRating = 40000
        self.currentStuff = 0
        self.start_time = time.time()
                
        if not os.path.exists('./output'):
            os.makedirs('./output')
        if not os.path.exists('./screens5000plus'):
            os.makedirs('./screens5000plus')

    def is_ascii(s):
        return all(ord(c) < 128 for c in s)

    def start(self):
        
        start_time = time.time()
        res = pd.read_csv("./newDf.csv", delimiter=",", usecols=["App Name", "App Id", "Category", "Rating", "Rating Count", "Installs","Developer Website", "Last Updated"])
        URL = "https://play.google.com/store/apps/details"
        dataset = res.iterrows()
        datasetLength = len(res.index)
        # Can be -1 if unlimited
        limitApps = 10001
        newDf = []
        print(res["Developer Website"].unique())
        

        class Runner(Thread):
            def __init__(self, index, i, ctx):
                Thread.__init__(self)
                self.index = index
                self.ctx = ctx
                self.i = i

            def run(self):
                PARAMS = {'id': i["App Id"]} 
                r = requests.get(url = URL, params = PARAMS) 
                data = r.text.replace("\n","").replace("\r","")
                regex = r"<img.*? src.*?=\"((https:\/\/play-lh.googleusercontent.com.*?))\""
                matches = re.finditer(regex, data, re.IGNORECASE)
                
                for matchNum, match in enumerate(matches, start=1):
                    if matchNum == 1 or matchNum == 2:
                        continue

                    for groupNum in range(0, len(match.groups())):
                        groupNum = groupNum + 1
                        if groupNum == 2: 
                            image_url = match.group(groupNum)
                            req = request.urlopen(image_url)
                            arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
                            image = cv2.imdecode(arr, -1) # 'Load it as it is'
                            height, width, channel = image.shape
                            if height <= width:
                                continue

                            if not path.exists("./screens5000plus/"+str(self.i["Rating"])+"/"):
                                os.mkdir("./screens5000plus/"+str(self.i["Rating"])+"/")
                            sys.stdout = open(os.devnull, 'w')
                            imsave("./screens5000plus/"+str(self.i["Rating"])+"/"+self.i["App Id"]+"."+str(matchNum)+".png", image)
                            sys.stdout = sys.__stdout__
                            self.ctx.currentStuff -= 1
                                
                try:
                    print("Done: " + self.i["App Name"])
                except:
                    print("No Encoding")
                    

            
            def contrast(self, image_path_arr, kn):
                for image_path in image_path_arr:
                    image = imread(image_path)

                    ed_sobel = filters.sobel(image)
                    
                    imgFit = [[[x[0] * x[1]] for x in feature_extraction.image.PatchExtractor(patch_size=(2, 2)).fit(image).transform(image)]]
                    kn.fit([[[x[0] * x[1]] for x in feature_extraction.image.PatchExtractor(patch_size=(2, 2)).fit(image).transform(image)]], [3.3])
                    print(kn.predict([x[0] * x[1] for x in feature_extraction.image.PatchExtractor(patch_size=(2, 2)).fit(image).transform(image)]))
                    imsave(image_path.replace("screens5000plus","screensContrast"), ed_sobel)

                              
        for index, i in dataset:
            
            while self.currentStuff >= 100:
                print("waiting")
                time.sleep(0.2)
           
            if not os.path.exists("./screens5000plus/"+str(i["Rating"])+"/" + i["App Id"] + "3.png"):
                self.count += 1
                self.currentStuff += 1
                Runner(index, i, self).start()

                    
                
        
        print("Timer: " + str(time.time() - start_time ))


Scrapper().start()
