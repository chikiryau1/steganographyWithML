from Image.Image import Img
from LSB.LSB import LSB
from KOHONEN.KOHONEN import Kohonen
from wavelets.wavelets import imageDWT, haarWavelet, getContrast, getGlobalContrast

class Steganography(object):

    def __init__(self, pathToImage, messageToEncrypt, encryptionMethod, pathToNewImage):
        self.image = Img(pathToImage)
        self.message = messageToEncrypt
        self.encryptionMethod = encryptionMethod
        self.newPath = pathToNewImage
        self.key = ''

    def encrypt(self):
        self.image.toArray()

        if (self.encryptionMethod == 'lsb'):
            l = LSB(self.image.RGB, self.message)
            l.encrypt()
            self.key = l.key
            self.image.RGB = l.image
            self.image.fromArrayToImage(self.newPath)

        if (self.encryptionMethod == 'kohonen'):
            self.image.divide(8,8)
            k = Kohonen(self.image.divided, self.message)          
            k.setContrastPoints()
            k.som(3, 1, 1, 5)
            k.encrypt()
            self.key = k.key
            self.image.divided = k.image
            self.image.joinBlocks()
            self.image.toImage(self.newPath)
   

    def decrypt(self):
        message = ''
        if (self.encryptionMethod == 'lsb'):
            image = Img(self.newPath)
            image.toArray()
            l = LSB(image.RGB, '')
            l.decrypt(image.RGB, self.key)
            message = l.decryptedMessage
        
        if (self.encryptionMethod == 'kohonen'):
            image = Img(self.newPath)
            image.toArray()  
            k = Kohonen(image, '')          
            image.divide(8,8)
            k.decrypt(image.divided, self.key)
            message = k.decryptedMessage
        return message