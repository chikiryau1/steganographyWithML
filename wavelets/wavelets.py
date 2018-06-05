import pywt
import numpy as np
import matplotlib.pyplot as plt
import math

def DWT(data):
    w = pywt.Wavelet('sym3')
    cA, cD = pywt.dwt(data, wavelet=w, mode='constant')
    print(cA, cD)        

def haarWavelet(vector, dm=1):
    if(dm == 1):
        l = len(vector) 
        print('to', l // 2)
        h = np.zeros((l // 2,), dtype='float64')
        g = np.zeros((l // 2,), dtype='float64')

        for e in range(len(h)):
            g[e] = (float(vector[e * 2]) + float(vector[e * 2 + 1])) / 2
            h[e] = (float(vector[e * 2]) - float(vector[e * 2 + 1])) / 2

        return {'highPass': h, 'lowPass': g}

    if(dm == 2):
        height, width = vector.shape
        # print(height, width)
        h = np.zeros((height, width // 2), dtype='float64')
        g = np.zeros((height, width // 2), dtype='float64')

        for k in range(height):
            for e in range(width // 2):
                # print(k, e)
                g[k][e] = (float(vector[k][e * 2]) + float(vector[k][e * 2 + 1])) / 2
                h[k][e] = (float(vector[k][e * 2]) - float(vector[k][e * 2 + 1])) / 2

        LL = np.zeros((width // 2, height // 2),  dtype='float64')
        HL = np.zeros((width // 2, height // 2),  dtype='float64')
        LH = np.zeros((width // 2, height // 2),  dtype='float64')
        HH = np.zeros((width // 2, height // 2),  dtype='float64')

        for k in range(width // 2):
            for e in range(height // 2):
                LL[e][k] = (float(g[e * 2][k]) + float(g[e * 2 + 1][k])) / 2
                HL[e][k] = (float(g[e * 2][k]) - float(g[e * 2 + 1][k])) / 2
                LH[e][k] = (float(h[e * 2][k]) + float(h[e * 2 + 1][k])) / 2                
                HH[e][k] = (float(h[e * 2][k]) - float(h[e * 2 + 1][k])) / 2
                
        
        return {'LL': LL, 'HL': HL, 'LH': LH, 'HH': HH}

def joinToRgb(r, g, b, dm=1):
    if dm == 1:
        h = len(r)
        img = np.zeros((h, 3), dtype='uint8')

        for i in range(h):
            img[i][0] = int(r[i])
            img[i][1] = int(g[i])
            img[i][2] = int(b[i])

        img1 = img.reshape(int(math.sqrt(len(img))), int(math.sqrt(len(img))), 3) 
        return img1

    if dm == 2:
        h, w = r.shape
        img = np.zeros((h, w, 3), dtype='uint8')

        for i in range(h):
            for j in range(w):
                img[i][j][0] = int(r[i][j])
                img[i][j][1] = int(g[i][j])
                img[i][j][2] = int(b[i][j])

        return img

def waveletPlots(vector, h, g):
    pass
    # x = np.arange(64)
    
    # plt.figure(1)
    # plt.subplot(311)
    # # plt.plot(x, vector, color='green')
    # plt.stem(x, vector)
    # plt.grid()

    # plt.subplot(312)
    # # plt.plot(x, h, linewidth=1, markersize=5)
    # plt.stem(x, h)
    # plt.grid()
    
    # plt.subplot(313) 
    # # plt.plot(x, g, 'bo-', linewidth=1, markersize=5, color='red')
    # plt.stem(x, g)

    # plt.grid()
    # plt.show()   
    # print(h)
    # print(g)
