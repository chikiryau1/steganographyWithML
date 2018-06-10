from LSB.LSB import LSB
from Image.Image import Img
from PIL import Image

from wavelets.wavelets import imageDWT, haarWavelet, getContrast, getGlobalContrast
import numpy   

def main():
    image = Img('testImages/4.2.03.tiff')
    image.toArray()
    image.divide(8, 8)
    
    # lsb = LSB(image.divided[0], 'Hello World!')
    # lsb.encrypt()
    # image.divided[0] = lsb.image

    # image.joinBlocks()
    # image.toImage('test1.tiff')

    # image2 = Img('test1.tiff')
    # image2.toArray()
    # image2.divide(8, 8)

    # lsb.decrypt(image2.divided[0], lsb.key)
    # print('message: ', lsb.decryptedMessage)
    
    # DWT(lsb.image)
    # ycbcr = image.toYCbCr()
    # print(ycbcr)

    # image = Img('testImages/4.2.03.tiff')
    # image.toArray()
    # imageDWT(image, 'BABOON_', 5)
    
    Image.fromarray(image.divided[0]).save('0.tiff')

    image0 = Img('0.tiff')
    image0.toArray()

    decomposed = imageDWT(image0, '', level=1)
    # print(decomposed)
    verticalContrast = getContrast(decomposed.get('LL'), decomposed.get('LH'))
    horizontalContrast = getContrast(decomposed.get('LL'), decomposed.get('HL'))
    diagonalContrast = getContrast(decomposed.get('LL'), decomposed.get('LH'))
    globalContrast = getGlobalContrast(verticalContrast, horizontalContrast, diagonalContrast)
    print('vertical:  ', verticalContrast)
    print('horizontal:  ', horizontalContrast)
    print('diagonal:  ', diagonalContrast)
    print('global:  ', globalContrast)
    
    
    

if __name__ == '__main__':
    main()


    

