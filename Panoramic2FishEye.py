from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

class Panoramic2FishEye:
    def __init__(self, imgWidth, imgHeight):
        self.imgWidth = imgWidth
        self.imgHeight = imgHeight
        
    def setPanoramicWithPath(self, imgPath):
        '''
        Works with color panoramic images
        '''
        
        self.img = np.asarray(Image.open(imgPath))/255.0
        

    def setPanoramic(self, img):
        self.img = img

    def getPanoramicImage(self):
        return self.img
        
        

    def convert2FishEye(self, radiusFraction):

        radius = radiusFraction*np.min([self.imgWidth, self.imgHeight])
        self.radius = radius
        midPointX = int(self.imgWidth/2)
        midPointY = int(self.imgHeight/2)

        fishImage = np.zeros((self.imgHeight, self.imgWidth,3))
        

        panoramicWidth = np.size(self.img,1)
        panoramicHeight = np.size(self.img,0)

        for i in range(0,self.imgHeight):
            for j in range(0,self.imgWidth):
                xa = j
                ya = i

                if(xa < midPointX):
                    index1 = int((np.sqrt((xa - midPointX)**2 + (ya - midPointY)**2)/radius)*panoramicHeight)
                    index2 = int((np.pi/2 + np.arctan((ya - midPointY)/(xa - midPointX)))*(panoramicWidth/(2*np.pi)))
                    fishImage[i,j,:] = self.img[index1, index2,:]

                elif(xa > midPointX):
                    index1 = int((np.sqrt((xa - midPointX)**2 + (ya - midPointY)**2)/radius)*panoramicHeight)
                    index2 = int((3*np.pi/2 + np.arctan((ya - midPointY)/(xa - midPointX)))*(panoramicWidth/(2*np.pi)))
                    fishImage[i,j,:] = self.img[index1, index2,:]

        return fishImage

        
                    
