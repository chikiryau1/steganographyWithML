import numpy as np
import matplotlib.pyplot as plt
import math
from PIL import Image

def haarWavelet(vector, dm=1):
    if(dm == 1):
        l = len(vector) 
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

def imageDWT(image, pathToNewImage, level=1):
    R = image.getRGBComponent(image.RGB, channel='R')
    B = image.getRGBComponent(image.RGB, channel='B')
    G = image.getRGBComponent(image.RGB, channel='G')

    HH, LL, LH, LL = '','','',''


    for l in range(1, level + 1):
        R = haarWavelet(R, 2)
        G = haarWavelet(G, 2)
        B = haarWavelet(B, 2)

        HH = image.joinToRgb(R.get('HH'), G.get('HH'), B.get('HH'), dm=2)
        HL = image.joinToRgb(R.get('HL'), G.get('HL'), B.get('HL'), dm=2)
        LH = image.joinToRgb(R.get('LH'), G.get('LH'), B.get('LH'), dm=2)
        LL = image.joinToRgb(R.get('LL'), G.get('LL'), B.get('LL'), dm=2)

        if(pathToNewImage != ''):
            topPart = np.concatenate((LL, HL), axis=1)
            bottomPart = np.concatenate((LH, HH), axis=1)
            Image.fromarray(np.concatenate((topPart, bottomPart), axis=0)).save(pathToNewImage + 'DWT_level_' + str(l) + '.tiff')

        R = R.get('LL')
        G = G.get('LL')
        B = B.get('LL')

    return {'LL': LL, 'HH': HH, 'LH': LH, 'HL': HL}

def getPixelBrightness(pixel):
    return 0.2126 * pixel[0] + 0.7152 * pixel[1] + 0.0722 * pixel[2]

def getContrast(backgroundArray, featureArray):
    h,w,_ = backgroundArray.shape
    vector = np.zeros(h * w)
    index = 0
    for i in range(h):
        for j in range(w):
            backgroundBrightness = getPixelBrightness(backgroundArray[i][j])
            featureBrightness = getPixelBrightness(featureArray[i][j])
            # print(backgroundArray[i][j], featureArray[i][j])
            vector[index] = (featureBrightness - backgroundBrightness) / backgroundBrightness if backgroundBrightness != 0 else 0
        
            index += 1
    
    return vector

def getGlobalContrast(vertical, horizontal, diagonal):
    h = len(vertical)
    c = np.zeros(h)
    for i in range(h):
        c[i] = vertical[i] + horizontal[i] + diagonal[i]

    return c

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
