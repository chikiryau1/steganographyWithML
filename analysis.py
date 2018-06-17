from Image.Image import Img
import numpy as np
import math 
class Analysis(object):

    def __init__(self, pathToOrigImage, pathToNewImage):
        original = Img(pathToOrigImage)
        stego = Img(pathToNewImage)
        original.toArray()
        stego.toArray()
        self.original = original.RGB
        self.stego = stego.RGB
        h,w,_ = self.original.shape
        self.numPixels = h * w

    def MSE(self):
        mse = 0
        meanStego = 0 
        meanOriginal = 0 
        h,w,_ = self.original.shape
        for i in range(h):
           for j in range(w):
               originalBrightness = 0.2126 * self.original[i][j][0] + 0.7152 * self.original[i][j][1] + 0.0722 * self.original[i][j][2]
               stegoBrightness = 0.2126 * self.stego[i][j][0] + 0.7152 * self.stego[i][j][1] + 0.0722 * self.stego[i][j][2]
               meanStego += stegoBrightness
               meanOriginal += originalBrightness
               mse += (originalBrightness - stegoBrightness)**2

        normMse = mse / self.numPixels
        meanStego /= self.numPixels
        meanOriginal /= self.numPixels
        
        self.meanStego = meanStego
        self.meanOriginal = meanOriginal
        self.mse = normMse

    def corr(self):
        cov = 0
        stegoNorm = 0
        originalNorm = 0
        originalStd = 0
        stegoStd = 0
        for i in range(len(self.original)):
            for j in range(len(self.original[i])):
                originalBrightness = 0.2126 * self.original[i][j][0] + 0.7152 * self.original[i][j][1] + 0.0722 * self.original[i][j][2]
                stegoBrightness = 0.2126 * self.stego[i][j][0] + 0.7152 * self.stego[i][j][1] + 0.0722 * self.stego[i][j][2]
                cov += (originalBrightness - self.meanOriginal) * (stegoBrightness - self.meanStego)

                originalStd += (originalBrightness - self.meanOriginal) ** 2
                stegoStd += (originalBrightness - self.meanOriginal) ** 2
                
                stegoNorm += stegoBrightness ** 2
                originalNorm += originalBrightness ** 2
        
        stegoNorm = math.sqrt(stegoNorm)
        originalNorm = math.sqrt(originalNorm)
       
        self.stegoStd = stegoStd
        self.originalStd = originalStd

        self.covariance = cov / self.numPixels        

        self.correlation = 1 - self.covariance / (stegoNorm * originalNorm)
    
    def SSIM(self):
        c1 = (0.01 * (2 ** 24 - 1))**2
        c2 = (0.03 *  (2 ** 24 - 1))**2
        
        self.ssim = (((2 * self.meanOriginal * self.meanStego + c1) * (self.covariance + c2)) /
        ((self.meanOriginal ** 2 + self.meanStego ** 2 + c1) * (self.stegoStd + self.originalStd + c2)))

    def Fusion(self):
        self.fusion = (self.correlation * self.ssim) / self.mse

    def Fusion1(self):
        self.fusion1 = self.correlation * self.ssim

    