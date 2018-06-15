from Image.Image import Img

class Analysis(object):

    def __init__(self, pathToOrigImage, pathToNewImage):
        self.original = Img(pathToOrigImage)
        self.stego = Img(pathToNewImage)

    def getMSE(self):
        pass
        
    def getCorr(self):
        pass

    def getSSIM(self):
        pass

    def getFusion(self):
        pass

    