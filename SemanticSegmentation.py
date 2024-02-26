import cv2
import numpy as np
import os 
import imutils
import torch
import sys
import DeepLabV3Plus.network
from PIL import Image
from torchvision import transforms


class SemanticSegmentation:

    def __init__(self):
        modelName = "deeplabv3plus_mobilenet"
        numClasses = 19
        outputStride = 8
        model = DeepLabV3Plus.network.modeling.__dict__[modelName](num_classes=numClasses, output_stride=outputStride)
        model.load_state_dict(torch.load('cityscapes_model.pth', map_location=torch.device('cpu'))['model_state'])
        self.model = model
        

    def segmentImage(self, imgArray):

        transform = transforms.ToTensor()
        inputImage = transform(imgArray)
        inputImage = inputImage.unsqueeze(0)
        self.model.eval()
        outputs = self.model(inputImage)
        preds = outputs.max(1)[1].detach().cpu().numpy()
        skyIndex = 10
        n = np.size(preds,1)
        m = np.size(preds,2)

        mask = np.zeros((n,m))
        for i in range(0,n):
            for j in range(0,m):
                if(preds[0,i,j] == skyIndex):
                    mask[i,j] = 1
        

        resizedMask = cv2.resize(mask, (np.size(imgArray,1), np.size(imgArray,0)),interpolation = cv2.INTER_NEAREST)
        maskedImg = imgArray.copy()
        for i in range(0,np.size(imgArray,0)):
            for j in range(0,np.size(imgArray,1)):
                maskedImg[i,j,:] = imgArray[i,j,:]*resizedMask[i,j]

        
        return maskedImg