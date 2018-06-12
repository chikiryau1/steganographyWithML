from LSB.LSB import LSB, textToBin
from Image.Image import Img
from PIL import Image
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from wavelets.wavelets import imageDWT, haarWavelet, getContrast, getGlobalContrast
import numpy   
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import math
def main():
    image = Img('testImages/4.2.03.tiff')
    image.toArray()
    # print(image.RGB.shape)
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
    # imageDWT(image, 'BABOON_', 1)

    # image = Img('testImages/4.2.05.tiff')
    # image.toArray()
    # imageDWT(image, 'AIRPLANE_', 1)
    
    # image = Img('testImages/4.2.06.tiff')
    # image.toArray()
    # imageDWT(image, 'SAILBOAT_', 1)
    # image = Img('testImages/4.2.07.tiff')
    # image.toArray()
    # imageDWT(image, 'PEPPERS_', 1)
    # index = 4070
    # print(image.divided.shape)

    contrastPoints = numpy.zeros(len(image.divided))

    for index in range(len(image.divided)):

        image0 = Img(path='', array=image.divided[index])
    
            
        # image0 = Img(str(index)+'.tiff')
        image0.toArray()

        decomposed = imageDWT(image0, '', level=1)
        # print(decomposed)
        verticalContrast = getContrast(decomposed.get('LL'), decomposed.get('LH'))
        horizontalContrast = getContrast(decomposed.get('LL'), decomposed.get('HL'))
        diagonalContrast = getContrast(decomposed.get('LL'), decomposed.get('LH'))
        globalContrast = getGlobalContrast(verticalContrast, horizontalContrast, diagonalContrast)
        # print('vertical:  ', verticalContrast)
        # print('horizontal:  ', horizontalContrast)
        # print('diagonal:  ', diagonalContrast)
        # print('global:  ', globalContrast)

        C = 0

        for i in globalContrast:
            C += i

        contrastPoints[index] = C if C < 150 else 0
        # Image.fromarray(image0.RGB).save(str(index) + '.tiff')
        # if(C > 120):
        #     print(index)
        # contrastPoints[index] = C

    # image.joinBlocks()
    # image.toImage('image.tiff') 
    
    # print(contrastPoints.reshape((64, 64)))

    fig = plt.figure()
    ax = fig.gca(projection='3d')

    # Make data.
    X = numpy.arange(0, int(math.sqrt(len(contrastPoints))), 1)
    Y = numpy.arange(0, int(math.sqrt(len(contrastPoints))), 1)
    X, Y = numpy.meshgrid(X, Y)

    Z = contrastPoints.reshape((int(math.sqrt(len(contrastPoints))), int(math.sqrt(len(contrastPoints)))))

    ax.set_xlabel('height number of block')
    ax.set_ylabel('width number of block')
    ax.set_zlabel('contrast')
    ax.scatter(X, Y, Z)

    plt.figure()
    plt.plot(numpy.arange(0, len(contrastPoints), 1), contrastPoints, 'o', ms=0.5)

    plt.show()

    # print(len(textToBin('Hello')))

if __name__ == '__main__':
    main()


    

