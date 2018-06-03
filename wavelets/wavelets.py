import pywt
import numpy as np
import matplotlib.pyplot as plt

def DWT(data):
    w = pywt.Wavelet('sym3')
    cA, cD = pywt.dwt(data, wavelet=w, mode='constant')
    print(cA, cD)        

def haarWavelet(vector):
    l = len(vector) 
    h = np.zeros((l,), dtype='float64')
    g = np.zeros((l,), dtype='float64')
    for e in range(len(h) // 2):
        h[e] = (float(vector[e * 2]) + float(vector[e * 2 + 1])) / 2
        g[e] = (float(vector[e * 2]) - float(vector[e * 2 + 1])) / 2

    x = np.arange(64)
    
    plt.figure(1)
    plt.subplot(311)
    # plt.plot(x, vector, color='green')
    plt.stem(x, vector)
    plt.grid()

    plt.subplot(312)
    # plt.plot(x, h, linewidth=1, markersize=5)
    plt.stem(x, h)
    plt.grid()
    
    plt.subplot(313) 
    # plt.plot(x, g, 'bo-', linewidth=1, markersize=5, color='red')
    plt.stem(x, g)

    plt.grid()
    plt.show()   
    print(h)
    print(g)
