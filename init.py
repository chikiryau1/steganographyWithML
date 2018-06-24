from Image.Image import Img
from wavelets.wavelets import imageDWT
from methods import Steganography
from analysis import Analysis
from tqdm import tqdm
from plots import barCharts, clasterisationPlots
from appData import get100BytesMessage, getDiploma, testImages, elmData, lsbData, kohonenData
    
def testImagesDWT():
    print('Images DWT calculation')
    for image in tqdm(testImages):
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
    
    kohonenAnalysisData = a.normalize(kohonenData) 
    print(lsbData)
    print(kohonenAnalysisData)
    barCharts(['baboon', 'airplane', 'peppers', 'earth'])
    
    
def allMethodsRun(message):
    for image in testImages:
        # --------------------------- LSB ---------------------------------------
        s = Steganography(image, message, 'lsb', 'encryptedLSB/' + testImages.get(image) + '.tiff')
        s.encrypt()
        m = s.decrypt()
        f = open('decryptedMessages/' + testImages.get(image) + '_LSB.txt', 'w')
        f.write(m)
        f.close()
        print('decrypted message', m)
        # --------------------------- /LSB ---------------------------------------

        # --------------------------- KOHONEN ---------------------------------------
        s = Steganography(image, message, 'kohonen', 'KOHONENencrypted/' + testImages.get(image) + '.tiff')
        s.encrypt()
        m = s.decrypt()
        f = open('decryptedMessages/' + testImages.get(image) + '_kohonen.txt', 'w')
        f.write(m)
        f.close()
        print('decrypted message', m)
        # --------------------------- /KOHONEN ---------------------------------------

def main():

    # message100Bytes = get100BytesMessage()
    # allMethodsRun(message100Bytes)
    
    # diploma = getDiploma()
    # allMethodsRun(diploma)

    # testImagesDWT()

    # clasterisationPlots()

    testImagesAnalyze()    
    
    
if __name__ == '__main__':
    main()


    

