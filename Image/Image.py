from PIL import Image
import numpy
import math

class Img(object):

    def __init__(self, path, array=[]):
        self.path = path
        self.img = Image.open(path) if path != '' else Image.fromarray(array)
    

    def toByteArray(self):
        """
            Returns image byte representation. 
        """
        # arr = self.toArray()

        # for x in arr:
        #     for y in x:
        #         for z in y:

        
    def setImageData(self, arrayOfPixels):
        pass

    def toYCbCr(self):
        return numpy.array(self.img.convert('YCbCr'))

    def toArray(self):
        """
            Sets image as array of RGB components. 
        """
        self.RGB = numpy.array(self.img) 
        del self.img 

    def getRGBComponent(self, arr, channel='R'):
        h, w, _ = arr.shape
        channelIndex = 0 if channel == 'R' else (1 if channel == 'G' else 2) 
        # print(channelIndex)
        arrChannel = numpy.zeros((h, w), dtype='uint8')
        for h in range(len(arr)):
            for w in range(len(arr[h])):
                arrChannel[h][w] = arr[h][w][channelIndex]
        return arrChannel

    def vectorizeChannel(self, channelArray):
        return channelArray.flatten()

    def toImage(self, path):
        """
            Method receives a RGB representation of image and
            writes it into file.
        """
        Image.fromarray(self.joined).save(path)
        # del self.joined  

    def divide(self, width, height):
        """
            Method divides an image to blocks with size width*height.
        """
        w, h, l = self.RGB.shape
        self.divided = self.RGB.reshape(int(w*h/(width*height)), width, height, l)  
        del self.RGB  

    def joinBlocks(self):
        """
            Method joins blocks from 4d array to array of pixels.
        """
        # print(self.divided.shape)
        numOfBlocks, w, h, l = self.divided.shape
        self.joined = self.divided.reshape(int(numOfBlocks/w), int(numOfBlocks/h), l)
        del self.divided

    def joinToRgb(self, r, g, b, dm=1):
        if dm == 1:
            h = len(r)
            img = numpy.zeros((h, 3), dtype='uint8')

            for i in range(h):
                img[i][0] = int(r[i])
                img[i][1] = int(g[i])
                img[i][2] = int(b[i])

            img1 = img.reshape(int(math.sqrt(len(img))), int(math.sqrt(len(img))), 3) 
            return img1

        if dm == 2:
            h, w = r.shape
            img = numpy.zeros((h, w, 3), dtype='uint8')

            for i in range(h):
                for j in range(w):
                    img[i][j][0] = int(r[i][j])
                    img[i][j][1] = int(g[i][j])
                    img[i][j][2] = int(b[i][j])

            return img

