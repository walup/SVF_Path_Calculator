from Panoramic2FishEye import Panoramic2FishEye
import matplotlib.pyplot as plt
import numpy as np


class SVFishCalculator:

    def obtainSVF(self, img, fishImageWidth, fishImageHeight, showFishImage = False):
        '''
        Receives a segmented image and gives the VCF metric
        
        '''
        fishImgConverter = Panoramic2FishEye(fishImageWidth, fishImageHeight)
        fishImgConverter.setPanoramic(img)
        radiusFraction = 1
        fishImage = fishImgConverter.convert2FishEye(radiusFraction, )
        if(showFishImage):
            plt.figure()
            plt.imshow(fishImage)
            plt.title("Fish-eye image")

        radius = fishImgConverter.radius

        n = np.size(fishImage,0)
        m = np.size(fishImage,1)
        totalPixels = 0
        occupiedPixels = 0
        midX = int(m/2)
        midY = int(n/2)
        for i in range(0,n):
            for j in range(0,m):
                dst = np.sqrt((j - midX)**2 + (i - midY)**2)
                if(dst < radius):
                    totalPixels = totalPixels + 1
                    if(not all(v == 0 for v in fishImage[i,j,:])):
                        occupiedPixels = occupiedPixels + 1

        return occupiedPixels/totalPixels
                
        