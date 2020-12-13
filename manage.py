from flask import Flask
from flask import Flask, redirect, url_for
from flask import Flask, render_template
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import ScorePrediction
from werkzeug.datastructures import  FileStorage
from pathlib import Path
import os
import shutil
from ImageSplitter import returnSplitAppImagesOfAllApps
from ImageSplitter import returnSplitImagesOfApp
import cv2
import time

app = Flask(__name__)

app.url_map.strict_slashes = False

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
  
    
    if request.method == 'POST':
        f = request.files['file'] 

        os.makedirs(os.path.join('uploads'), exist_ok=True)
        dirList = os.listdir('uploads/')
        
        filename = secure_filename(f.filename)
       
        if Path(filename).suffix == ".png" or Path(filename).suffix == ".jpg" or Path(filename).suffix == ".jpeg":
           
            
            
            #f.save(filename) # secure_filename('app' + str(imgNum) + Path(f.filename).suffix)
            os.makedirs(os.path.join(app.instance_path, 'htmlfi'), exist_ok=True)
            imgNum = len(list(app.instance_path))
            f.save(os.path.join(app.instance_path, 'htmlfi', secure_filename(f.filename))) # 'app' + str(imgNum) + Path(filename).suffix))
            #f.save(os.path.join(app.config['uploads/'], )
            #shutil.move(filename, 'uploads/' + 'appImg' + str(len(dirList)) + Path(filename).suffix)
            

    return "good"

@app.route('/score', methods = ['GET', 'POST'])
def request_score():

  
    if request.method == 'GET':
       
        time.sleep(3)
        

       
        index = 0
        dir = app.instance_path +'/htmlfi'
        for filename in os.listdir(dir):
           
            fileType = Path(filename).suffix
            os.rename(app.instance_path +'\\htmlfi' + '\\' + filename, app.instance_path +'\\htmlfi' + '\\' + 'appImg' + str(index) + fileType)
           
            index += 1

       
        appId = "appImg"
        dir = app.instance_path +'/htmlfi'
        

        singleAppImageData = returnSplitImagesOfApp(appId, dir)

        croppedImgs = []
        for a in singleAppImageData:
          
            for b in singleAppImageData[a]:
                
                for c in singleAppImageData[a][b]:
                  
                    for d in c:
                       
                        index = 0
                        for e in range(len(c[d])):
                            croppedImg = c[d][e]
                            print('index ' + str(index))
                            #cv2.destroyAllWindows()
                            #cv2.imshow('croppedImg', croppedImg) 
                            #cv2.waitKey(1)
                            #time.sleep(0.5) 
                            croppedImgs.append(croppedImg) 
                            index += 1

                            
        return ScorePrediction.getScore(croppedImgs)
    return 'no data'

@app.route('/', methods=['GET', 'POST'])
def hello():
    return render_template("welcome.html")


if __name__ == "__main__":
    app.run()
