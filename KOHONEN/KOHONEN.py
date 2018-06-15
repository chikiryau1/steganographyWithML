from wavelets.wavelets import imageDWT, haarWavelet, getContrast, getGlobalContrast
from Image.Image import Img
import numpy   
from som import SOM

class Kohonen(object):

    def __init__(self, image, message):
        self.image = image
        self.message = message

    def encrypt(self):
        """
            Encrypt method.
        """
        messageStep = 0
        msg = textToBin(self.message)
        self.key = len(msg)


        for block, blockClassMap in zip(self.image, self.blocksMapping): 
            blockClass = blockClassMap[0] + blockClassMap[1]

            if(messageStep == len(msg)):
                break

            # blockClassToEmbed = '00'
            if (blockClass == self.mappingDict.get('most')):
                blockClassToEmbed = '00'
                # bitsToSubstitute = msg[messageStep]

            if (blockClass == self.mappingDict.get('mean')):
                blockClassToEmbed = '01'
                # bitsToSubstitute = msg[messageStep]
            
            if (blockClass == self.mappingDict.get('least')):
                blockClassToEmbed = '10'
                # bitsToSubstitute = [msg[messageStep], msg[messageStep]]                
            
            for i in range(len(block)):
                
                if(messageStep == len(msg)):
                    break

                for j in range(len(block[i])):

                    if(messageStep == len(msg)):
                        break

                    if (i == 0 and j == 0):
                        block[i][j][0] = int(self.substitute(get_bin(block[i][j][0], 8), blockClassToEmbed[0]), 2)
                        block[i][j][1] = int(self.substitute(get_bin(block[i][j][0], 8), blockClassToEmbed[1]), 2)                        
                        continue

                    if (blockClass == self.mappingDict.get('most')):
                        continue

                    for channel in range(len(block[i][j])):
                
                        if (blockClass == self.mappingDict.get('mean')):
                            bitsToSubstitute = msg[messageStep]
                        
                        if (blockClass == self.mappingDict.get('least')):
                            bitsToSubstitute = [msg[messageStep], msg[messageStep + 1]]
                        block[i][j][channel] = int(self.substitute(get_bin(block[i][j][channel], 8), bitsToSubstitute), 2)
                        d = list(self.mappingDict.keys())[list(self.mappingDict.values()).index(blockClass)]
                        messageStep += 1 if d == 'mean' else 2
                        if(messageStep == len(msg)):
                            break

    def substitute(self, changeByte, embedData):
        """
            Method receives changeByte and replaces lsbs with embedData according to its length.
        """
        data = list(changeByte)
        data[len(data)-1] = embedData

        for b in range(len(embedData)):
            # print(len(data) - len(embedData) + b, 'to', b)
            data[len(data) - len(embedData) + b] = embedData[b] 
        return ''.join(data)
        
    def decrypt(self, data, key):
        """
            Decrypt method. data: (N, x, y, 3)-shape array, key - length of embed message(just for now).
        """
        messageStep = 0
        msg = ''
        for block in data: 
            blockClass = ''  
            if(messageStep == key):
                break

            if (blockClass == '00'):
                continue

            # print(blockClass, len(block), len(block[0]))
            
            for i in range(len(block)):
                if(messageStep == key):
                    break
                for j in range(len(block[i])):
                    if(messageStep == key):
                        break
                    
                    if (i == 0 and j == 0):
                        extracted = get_bin(block[0][0][0],  8)
                        blockClass += extracted[len(extracted) - 1:]
                        extracted = get_bin(block[0][0][1],  8)
                        blockClass += extracted[len(extracted) - 1:]
                        continue

                    else:
                        if (blockClass == '01'):
                            step = 1
                            # messageStep += 1
                            # continue
                        if (blockClass == '10'):
                            step = 2
                            # messageStep += step
                            # continue

                    # print(blockClass)
                    for channel in range(len(block[i][j])):
                        extracted = get_bin(block[i][j][channel],  8)
                        msg += extracted[len(extracted) - step:]
                        messageStep += step
                        if(messageStep == key):
                            break
        self.decryptedMessage = frombits(msg)
    
    def setContrastPoints(self):
        # steps 1 - 3
        image = self.image
        contrastPoints = numpy.zeros(len(image))
        horizontalContrastPoints = numpy.zeros(len(image))
        verticalContrastPoints = numpy.zeros(len(image))
        diagonalContrastPoints = numpy.zeros(len(image))

        for index in range(len(image)):

            image0 = Img(path='', array=image[index])
            image0.toArray()
            decomposed = imageDWT(image0, '', level=1)
            verticalContrast = getContrast(decomposed.get('LL'), decomposed.get('LH'))
            horizontalContrast = getContrast(decomposed.get('LL'), decomposed.get('HL'))
            diagonalContrast = getContrast(decomposed.get('LL'), decomposed.get('LH'))
            globalContrast = getGlobalContrast(verticalContrast, horizontalContrast, diagonalContrast)

            C = 0

            sumVertical = 0
            sumHorizontal = 0
            sumDiagonal = 0
            

            for i in globalContrast:
                C += i
            
            for j in range(len(verticalContrast)):
                sumDiagonal += diagonalContrast[j]
                sumVertical += verticalContrast[j]
                sumHorizontal += horizontalContrast[j]
                
            contrastPoints[index] = C if C < 150 else 0
            horizontalContrastPoints[index] = sumHorizontal / len(horizontalContrast) if sumHorizontal < 50 else 0
            verticalContrastPoints[index] = sumVertical / len(verticalContrast) if sumVertical < 50 else 0
            diagonalContrastPoints[index] = sumDiagonal / len(diagonalContrast) if sumDiagonal < 50 else 0

        self.horizontalContrast = horizontalContrastPoints
        self.verticalContrast = verticalContrastPoints
        self.diagonalContrast = diagonalContrastPoints
        
        self.contrastPoints = contrastPoints

    def som3(self, m, n, dim, iterations):
        # step 4
        trainData = numpy.zeros((len(self.contrastPoints), 3))

        for i in range(len(self.contrastPoints)):
            trainData[i] = [self.diagonalContrast[i], self.verticalContrast[i], self.horizontalContrast[i]]

        som = SOM(m, n, dim, iterations)
        som.train(trainData)    
        mapped = som.map_vects(trainData)
        d0 = 0
        d1 = 0
        d2 = 0

        for d, m in zip(trainData, mapped):
            mapv = m[0] + m[1]
            
            if (d0 == 0 and mapv == 0):
                d0 = d[0] if d0 < d[0] else d0

            if (d1 == 0  and mapv == 1):    
                d1 = d[0] if d1 < d[0] else d1
                
            if (d2 == 0  and mapv == 2): 
                d2 = d[0] if d2 < d[0] else d2
                
        arr = numpy.array([d0, d1, d2])
        most = numpy.argmax(arr)
        numpy.delete(arr, most, 0)
        least = numpy.argmin(arr)
        numpy.delete(arr, least, 0)
        mean = 0 if (arr[most] == d1 or arr[most] == d2) and (arr[least] == d1 or arr[least] == d2) else (1 if (arr[most] == d0 or arr[most] == d2) and (arr[least] == d0 or arr[least] == d2) else 2)
        self.mappingDict = {'least':  least, 'mean': mean, 'most': most}  
        self.blocksMapping = mapped

    def som(self, m, n, dim, iterations):
        # step 4
        trainData = numpy.zeros((len(self.contrastPoints), 1))

        for i in range(len(self.contrastPoints)):
            trainData[i] = [self.contrastPoints[i]]

        som = SOM(m, n, dim, iterations)
        som.train(trainData)    
        mapped = som.map_vects(trainData)
        d0 = 0
        d1 = 0
        d2 = 0

        for d, m in zip(trainData, mapped):
            mapv = m[0] + m[1]
            
            if (d0 == 0 and mapv == 0):
                d0 = d[0] if d0 < d[0] else d0

            if (d1 == 0  and mapv == 1):    
                d1 = d[0] if d1 < d[0] else d1
                
            if (d2 == 0  and mapv == 2): 
                d2 = d[0] if d2 < d[0] else d2
                
        least = 0 if d0 < d1 and d0 < d2 else (1 if d1 < d0 and d1 < d2 else (2 if d2 < d1 and d2 < d0 else 0))
        most = 0 if d0 > d1 and d0 > d2 else (1 if d1 > d0 and d1 > d2 else (2 if d2 > d1 and d2 > d0 else 0))
        mean = 0 if d0 > d1 and d0 < d2 else (1 if d1 > d0 and d1 < d2 else (2 if d2 > d1 and d2 < d0 else 0))
        print(d0, d1, d2)
        print(least, most, mean)
        self.mappingDict = {'least':  least, 'mean': mean, 'most': most}  
        self.blocksMapping = mapped
        
def textToBin(text):
    return ''.join(str(x) for x in list(map(int, ''.join([bin(ord(i)).lstrip('0b').rjust(8,'0') for i in text]))))

def get_bin(x, n=0):
    return format(x, 'b').zfill(n)

def frombits(bits):
    chars = []
    for b in range(len(bits) // 8):
        byte = bits[b*8:(b+1)*8]
        chars.append(chr(int(''.join([str(bit) for bit in byte]), 2)))
    return ''.join(chars)


def format_data(string):
    return bin(int.from_bytes(string.encode(), 'big'))


def reformat_data(string):
    n = int(string, 2)
    return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode()