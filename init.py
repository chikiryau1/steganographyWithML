from LSB.LSB import LSB
from Image.Image import Img
from wavelets.wavelets import DWT,  haarWavelet, joinToRgb
from PIL import Image
import numpy

def imageWaveletDecomposition(pathToImage, pathToNewImage, level=1):
    image = Img(pathToImage)
    image.toArray()
    
    if level == 1:
        r1 = haarWavelet(image.getRGBComponent(image.RGB, channel='R'), 2)
        g1 = haarWavelet(image.getRGBComponent(image.RGB, channel='G'), 2)
        b1 = haarWavelet(image.getRGBComponent(image.RGB, channel='B'), 2)

        HH = joinToRgb(r1.get('HH'), g1.get('HH'), b1.get('HH'), dm=2)
        HL = joinToRgb(r1.get('HL'), g1.get('HL'), b1.get('HL'), dm=2)
        LH = joinToRgb(r1.get('LH'), g1.get('LH'), b1.get('LH'), dm=2)
        LL = joinToRgb(r1.get('LL'), g1.get('LL'), b1.get('LL'), dm=2)
        
        topPart = numpy.concatenate((LL, HL), axis=1)
        bottomPart = numpy.concatenate((LH, HH), axis=1)

        Image.fromarray(numpy.concatenate((topPart, bottomPart), axis=0)).save(pathToNewImage)

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

    # haarWavelet(image.vectorizeChannel(image.getRGBComponent(image.divided[0], channel='G')))
    imageWaveletDecomposition('testImages/4.2.03.tiff', 'test2.tiff')

if __name__ == '__main__':
    main()


    

