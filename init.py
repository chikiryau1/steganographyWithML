from Image.Image import Img
from PIL import Image
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from wavelets.wavelets import imageDWT, haarWavelet, getContrast, getGlobalContrast
import numpy   
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import math
from som import SOM
from methods import Steganography
from KOHONEN.KOHONEN import Kohonen

def getContrastPoints(image):

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

    return contrastPoints

def contrastPointsPlots(contrastPoints, mapping=''):
    # fig = plt.figure()
    # ax = fig.gca(projection='3d')

    # Make data.
    # X = numpy.arange(0, int(math.sqrt(len(contrastPoints))), 1)
    # Y = numpy.arange(0, int(math.sqrt(len(contrastPoints))), 1)
    # X, Y = numpy.meshgrid(X, Y)

    # Z = contrastPoints.reshape((int(math.sqrt(len(contrastPoints))), int(math.sqrt(len(contrastPoints)))))

    # ax.set_xlabel('height number of block')
    # ax.set_ylabel('width number of block')
    # ax.set_zlabel('contrast')
    # ax.scatter(X, Y, Z)

    x = numpy.arange(0, len(contrastPoints), 1)
    y = contrastPoints
    plt.figure()

    if mapping != '':
        for _x, _y, col in zip(x, y, mapping):
            # print(col)
            c = col[0] + col[1]   
            color = 'red' if c == 0 else ('green' if c == 1 else 'blue')
            plt.scatter(_x, _y, marker='o', c=color)
    else:
        plt.plot(numpy.arange(0, len(contrastPoints), 1), contrastPoints, 'o', ms=0.5)

    plt.show()

    # print(len(textToBin('Hello')))

def plot3d(x, y, z, mapping=''):
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    
    if mapping != '':
        for _x, _y, _z, m in zip(x, y, z, mapping):
            c = m[0] + m[1] 
            color = 'red' if c == 0 else ('green' if c == 1 else 'blue')              
            ax.scatter(_x, _y, _z, c=color, s=0.7)
    else:
        ax.scatter(x, y, z)
    
    ax.set_xlabel('mean horizontal contrast')
    ax.set_ylabel('mean diagonal contrast')
    ax.set_zlabel('mean vertical contrast')    
    plt.show()

def som(m, n, dim, iterations, data):
    som = SOM(m, n, dim, iterations)
    som.train(data)
    image_grid = som.get_centroids()
    grid = numpy.zeros((len(image_grid), 2))
   
    for i in range(len(image_grid)):
        grid[i] = [i, image_grid[i][0]]
   
    mapped = som.map_vects(data)
    return mapped

def testTrain():
    #Training inputs for RGBcolors
    colors = numpy.array(
        [[0., 0.],
        [0., 0.],
        [0., 0.],
        [0.125, 0.529],
        [0.33, 0.4],
        [0.6, 0.5],
        [0., 1.],
        [1., 0.],
        [0., 1.],
        [1., 0.],
        [1., 1.],
        [1., 1.],
        [.33, .33],
        [.5, .5],
        [.66, .66]])
    color_names = \
        ['black', 'blue', 'darkblue', 'skyblue',
        'greyblue', 'lilac', 'green', 'red',
        'cyan', 'violet', 'yellow', 'white',
        'darkgrey', 'mediumgrey', 'lightgrey']
    
    #Train a 20x30 SOM with 400 iterations
    som = SOM(20, 30, 3, 400)
    som.train(colors)
    
    #Get output grid
    image_grid = som.get_centroids()
    
    #Map colours to their closest neurons
    mapped = som.map_vects(colors)
    print(image_grid[0][0])
    #Plot
    plt.imshow(image_grid)
    plt.title('Color SOM')
    for i, m in enumerate(mapped):
        plt.text(m[1], m[0], color_names[i], ha='center', va='center',
                bbox=dict(facecolor='white', alpha=0.5, lw=0))
    plt.show()

def main():
    # --------------------------- LSB ---------------------------------------
    # s = Steganography('testImages/4.2.03.tiff', 'Hello World! Hello World! Hello World! Hello World! Hello World!', 'lsb', 'newBaboon.tiff')
    # s.encrypt()
    # print(s.decrypt())
    # --------------------------- /LSB ---------------------------------------

    # --------------------------- KOHONEN ---------------------------------------
    s = Steganography('testImages/4.2.03.tiff', 'Hello World! Hello World! Hello World! Hello World! Hello World!', 'kohonen', 'newBaboon.tiff')
    s.encrypt()
    print(s.decrypt())
    # --------------------------- /KOHONEN ---------------------------------------
    # image = Img('testImages/4.2.03.tiff')
    # image.toArray()
    # image.divide(8, 8)
    # k = Kohonen(image.divided, '')          
    # k.setContrastPoints()
    # k.som3(3, 1, 3, 10)
    # plot3d(k.horizontalContrast, k.diagonalContrast, k.verticalContrast)
    # plot3d(k.horizontalContrast, k.diagonalContrast, k.verticalContrast, k.blocksMapping3)
    
    # image = Img('testImages/4.2.03.tiff')
    # image.toArray()
    # image.divide(8, 8)
    # print(image.divided.shape)
    # contrastPoints = getContrastPoints(image)
    # contrastPointsPlots(contrastPoints)

    # trainData = numpy.zeros((len(contrastPoints), 1))

    # for i in range(len(contrastPoints)):
        # trainData[i] = [contrastPoints[i]]

    # print(trainData.shape, trainData[0])

    # mapped = som(3, 1, 1, 50, trainData)
    # contrastPointsPlots(contrastPoints, mapped)
    # testTrain()


    

    # image.divided[0] = lsb.image

    # image.joinBlocks()
    # image.toImage('test1.tiff')

    # image2 = Img('test1.tiff')
    # image2.toArray()
    # image2.divide(8, 8)
    
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

    # image.joinBlocks()
    # image.toImage('image.tiff') 
    
    # print(contrastPoints.reshape((64, 64)))

   

if __name__ == '__main__':
    main()


    

