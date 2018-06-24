from tqdm import tqdm
import numpy   
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from appData import lsbData, kohonenData, dataList, testImages, elmData
from Image.Image import Img
from KOHONEN.KOHONEN import Kohonen



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