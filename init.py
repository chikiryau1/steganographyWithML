from LSB.LSB import LSB
from Image.Image import Img
from wavelets.wavelets import DWT, plot_wavelet_decomposition, iwt2

def main():
    image = Img('testImages/4.2.03.tiff')
    image.toArray()
    # image.divide(8, 8)
    
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

    print(image.RGB[0])
    plot_wavelet_decomposition(image.RGB)


if __name__ == '__main__':
    main()