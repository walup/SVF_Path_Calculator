from GooglePhotoRetriever import GooglePhotoRetriever
from PIL import Image
from SemanticSegmentation import SemanticSegmentation
from Panoramic2FishEye import Panoramic2FishEye
import matplotlib.pyplot as plt
import numpy as np
from SVFCalculator import SVFishCalculator
from Panoramic2FishEye import Panoramic2FishEye
import time

class TrajectorySVFf:

    def __init__(self, points):
        self.trajectoryPoints = points
        self.fishWidth = 1000
        self.fishHeight = 1000

    def getSVFForTrajectory(self, baseURL, key):
        self.svfArray = []
        googleRetriever = GooglePhotoRetriever(key)
        segmentator = SemanticSegmentation()
        svFishCalculator = SVFishCalculator()
        fishImgConverter = Panoramic2FishEye(self.fishWidth, self.fishHeight)
        
        self.fishArray = np.zeros((np.size(self.trajectoryPoints,0), self.fishHeight, self.fishWidth, 3))
        for i in range(0,np.size(self.trajectoryPoints,0)):
            point = self.trajectoryPoints[i,:]
            googleRetriever.obtainImages("Google_Images", point[0],point[1])
            url = baseURL + "/panoramica_"+str(i)+".jpg"
            googleRetriever.stitchImages(url, googleRetriever.paths)
            time.sleep(3)
            img = np.asarray(Image.open(url))[:,:,0:3]
            fishImgConverter.setPanoramic(img)
            imgFish = fishImgConverter.convert2FishEye(1)
            self.fishArray[i,:,:,:] = imgFish
            maskedImage = segmentator.segmentImage(img)/255.0
            
            svff = svFishCalculator.obtainSVF(maskedImage, self.fishWidth, self.fishHeight, False)
            self.svfArray.append(svff)