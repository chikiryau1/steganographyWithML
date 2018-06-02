import pywt
import numpy as np
import matplotlib.pyplot as plt

def DWT(data):
    w = pywt.Wavelet('sym3')
    cA, cD = pywt.dwt(data, wavelet=w, mode='constant')
    print(cA, cD)        

def plot_wavelet_decomposition(image, level=1):
    """
    Plot of 2D wavelet decompositions for given number of levels.

    image needs to be either a colour channel or greyscale image:
        rgb: self.I[:, :, n], where n = {0, 1, 2}
        greyscale: use rgb_to_grey(self.I)

    """
    coeffs = pywt.wavedec2(image, wavelet='haar', level=level)
    # print(coeffs[0])
    for i, (cH, cV, cD) in enumerate(coeffs[1:]):
        if i == 0:
            cAcH = np.concatenate((coeffs[0], cH), axis=1)
            cVcD = np.concatenate((cV, cD), axis=1)
            plot_image = np.concatenate((cAcH, cVcD), axis=0)
        else:
            plot_image = np.concatenate((plot_image, cH), axis=1)
            cVcD = np.concatenate((cV, cD), axis=1)
            plot_image = np.concatenate((plot_image, cVcD), axis=0)

    plt.grid(False)
    # print(plot_image[0])
    plt.imshow(abs(plot_image))
    plt.show() 

def haarWavelet(vector):
    h = np.array()
    g = np.array()
    for e in range(vector):
        h.append((vector[e] + vector[e+1]) / 2)
        g.append((vector[e] - vector[e+1]) / 2)
        e += 1 

def _iwt(array):
    output = np.zeros_like(array)
    nx, ny = array.shape
    x = nx // 2
    for j in range(ny):
        output[0:x,j] = (array[0::2,j] + array[1::2,j])//2
        output[x:nx,j] = array[0::2,j] - array[1::2,j]
    return output

def _iiwt(array):
    output = np.zeros_like(array)
    nx, ny = array.shape
    x = nx // 2
    for j in range(ny):
        output[0::2,j] = array[0:x,j] + (array[x:nx,j] + 1)//2
        output[1::2,j] = output[0::2,j] - array[x:nx,j]
    return output

def iwt2(array):
    return _iwt(_iwt(array.astype(int)).T).T

def iiwt2(array):
    return _iiwt(_iiwt(array.astype(int).T).T)
