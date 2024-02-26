import google_streetview.api
import numpy as np
import time
from PIL import Image
import cv2

class GooglePhotoRetriever:

    def __init__(self, devKey):
        self.devKey = devKey
        self.pitch = 25
        self.nImages = 6
        self.angles = np.linspace(0,180, self.nImages)
        self.size = '600x300'

    def obtainImages(self,outputPath, coord1, coord2):
        coordString = str(coord1)+","+str(coord2)
        self.paths = []
        for i in range(0,len(self.angles)-1):
            params = [{'size': self.size,'location': coordString, 'heading':self.angles[i],'pitch':str(self.pitch),'key':self.devKey}]
            results = google_streetview.api.results(params)
            self.paths.append(outputPath + "/"+str(i)+"/gsv_0.jpg")
            results.download_links(outputPath + "/"+str(i))
            time.sleep(3)

    def stitchImages(self, outputPath, paths):
        images = []
        for i in range(0,len(paths)):
            image = cv2.imread(paths[i])
            images.append(image)

        stitcher = cv2.Stitcher_create()
        status, result = stitcher.stitch(images)
        
        cv2.imwrite(outputPath, result)