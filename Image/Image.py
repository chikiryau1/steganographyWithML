from PIL import Image
import numpy

class Img(object):

    def __init__(self, path):
        self.path = path
        self.img = Image.open(path)

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

    def getR(self):
        pass

    def getG(self):
        pass

    def getB(self):
        pass

    def toImage(self, path):
        """
            Method receives a RGB representation of image and
            writes it into file.
        """
        Image.fromarray(self.joined).save(path)
        del self.joined  

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