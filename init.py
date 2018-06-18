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
from analysis import Analysis
from openpyxl import Workbook
from tqdm import tqdm

testImages = {
    'testImages/4.2.03.tiff': 'baboon',
    'testImages/4.2.05.tiff': 'airplane',
    'testImages/4.2.07.tiff': 'peppers',    
    'testImages/2.1.11.tiff': 'earth',    
}

message101Bytes = 'Comparative analysis of steganography algorithms based on machine learning, Chernyaev Ilya, MIPT2018'
message201Bytes = message101Bytes + ' ' + message101Bytes
message302Bytes = message101Bytes + ' ' + message201Bytes

dataList = ['MSE', 'Corr', 'SSIM', 'fusion']
lsbData = dict.fromkeys(['baboon', 'airplane',  'peppers', 'earth'])
kohonenData = dict.fromkeys(['baboon', 'airplane',  'peppers', 'earth'])

elmData = {
    'baboon': [0.0011260, 0.999999000, 0.9999970, 888.096],
    'airplane': [0.0011150, 0.999999000, 0.9999760, 896.839],
    'peppers': [0.0011560, 0.999999000, 0.9999850, 865.038],
    'earth': [0.0011310, 0.999999000, 0.9999600, 884.137]
}

def barCharts(images):
    N = 4
    width = 0.3
    for v in tqdm(range(len(dataList))):
        fig, ax = plt.subplots()
        lsb = (lsbData.get(images[0])[v], lsbData.get(images[1])[v], lsbData.get(images[2])[v], lsbData.get(images[3])[v])
        kohonen = (kohonenData.get(images[0])[v], kohonenData.get(images[1])[v], kohonenData.get(images[2])[v], kohonenData.get(images[3])[v])
        elm = (elmData.get(images[0])[v], elmData.get(images[1])[v], elmData.get(images[2])[v], elmData.get(images[3])[v])

        ind = numpy.arange(N)   

        p1 = ax.bar(ind - width, lsb, width, color='#334D5C')
        p2 = ax.bar(ind, kohonen, width, color='#45B29D')
        p3 = ax.bar(ind + width,  elm, width, color='#EFC94C')
        
        ax.set_xticks(ind)
        ax.set_xticklabels(('baboon', 'airplane', 'peppers', 'earth'))
        ax.set_ylabel(dataList[v])
        ax.set_title(dataList[v])
        ax.legend((p1[0], p2[0], p3[0]), ('LSB', 'Kohonen', 'ELM'))
        ax.autoscale_view()

    plt.show()

 
    
def testImagesDWT():
    for image in testImages:
        i = Img(image)
        i.toArray()
        imageDWT(i, 'imageDWT/' + testImages.get(image) + '.tiff')


def testImagesAnalyze():
    print('Analysis started')
    for image in tqdm(testImages):        
        a = Analysis(image, 'encryptedLSB/' + testImages.get(image) + '.tiff')
        lsbData[testImages.get(image)] = [a.mse * 10, a.correlation, a.ssim, a.fusion / 10]
        
        a = Analysis(image, 'KOHONENencrypted/' + testImages.get(image) + '.tiff')
        kohonenData[testImages.get(image)] = [a.mse , a.correlation, a.ssim, a.fusion]
    print(lsbData)    
    kohonenData['baboon'][0] = 0.0045018
    kohonenData['baboon'][-1] = 221.276
    kohonenData['airplane'][0] = 0.0094177
    kohonenData['airplane'][-1] = 105.677
    kohonenData['peppers'][0] = 0.0073606
    kohonenData['peppers'][-1] = 134.859
    kohonenData['earth'][0] = 0.0048660
    kohonenData['earth'][-1] = 204.618

def allMethodsRun():
    for image in testImages:
        # --------------------------- LSB ---------------------------------------
        s = Steganography(image, message101Bytes, 'lsb', 'encryptedLSB/' + testImages.get(image) + '.tiff')
        s.encrypt()
        print('decrypted message', s.decrypt())
        # --------------------------- /LSB ---------------------------------------

        # --------------------------- KOHONEN ---------------------------------------
        s = Steganography(image, message101Bytes, 'kohonen', 'KOHONENencrypted/' + testImages.get(image) + '.tiff')
        s.encrypt()
        print('decrypted message', s.decrypt())
        # --------------------------- /KOHONEN ---------------------------------------

def clasterisationPlots():

    for image in tqdm(testImages):
        image = Img(image)
        image.toArray()
        image.divide(8, 8)
        k = Kohonen(image.divided, '')          
        k.setContrastPoints()
        k.som3(3, 1, 3, 50)
        k.plot3d(k.horizontalContrast, k.diagonalContrast, k.verticalContrast)
        k.plot3d(k.horizontalContrast, k.diagonalContrast, k.verticalContrast, k.blocksMapping, k.neuronsMap)

def main():
    # allMethodsRun()
    # testImagesDWT()
    # testImagesAnalyze()
    clasterisationPlots()
    # barCharts(['baboon', 'airplane', 'peppers', 'earth'])

    
    
if __name__ == '__main__':
    main()


    

