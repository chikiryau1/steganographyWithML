import bitarray

class LSB(object):

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
        # print('length: ' ,self.key, '\n', msg[15:])
        for i in range(len(self.image) - 1):
            if(messageStep == len(msg)):
                break
            for j in range(len(self.image[i]) - 1):
                if(messageStep == len(msg)):
                    break
                for channel in range(len(self.image[i][j])):
                    self.image[i][j][channel] = int(self.substitute(get_bin(self.image[i][j][channel], 8), msg[messageStep]), 2)
                    # print(msg[messageStep], '-------', messageStep)
                    messageStep += 1
                    if(messageStep == len(msg)):
                        break
 
    def substitute(self, changeByte, embedData):
        """
            Method receives changeByte and replaces lsbs with embedData according to its length.
        """
        # print(changeByte, '\n', embedData)
        data = list(changeByte)
        data[len(data)-1] = embedData
        return ''.join(data)
        
    def decrypt(self, data, key):
        """
            Decrypt method. data: (x, y, 3)-shape array, key - length of embed message(just for now).
        """
        messageStep = 0
        msg = ''
        for i in range(len(data) - 1):
            if(messageStep == key):
                break
            for j in range(len(data[i])):
                if(messageStep == key):
                    break
                for channel in range(len(data[i][j])):
                    extracted = get_bin(data[i][j][channel], 8)
                    msg += extracted[len(extracted) - 1:]
                    # print(extracted[len(extracted) - 1:], '======', messageStep)
                    messageStep += 1
                    if(messageStep == key):
                        break
        self.decryptedMessage = frombits(msg)
        # print(frombits('01110011'))

def textToBin(text):
    return ''.join(str(x) for x in list(map(int, ''.join([bin(ord(i)).lstrip('0b').rjust(8,'0') for i in text]))))

def get_bin(x, n=0):
    return format(x, 'b').zfill(n)

def frombits(bits):
    # ba = bitarray.bitarray(bits)
    # print(ba)
    # return ba.tobytes().decode('utf-8')
    chars = []
    for b in range(len(bits) // 8):
        byte = bits[b*8:(b+1)*8]
        print(chr(int(''.join([str(bit) for bit in byte]), 2)))
        chars.append(chr(int(''.join([str(bit) for bit in byte]), 2)))
    return ''.join(chars)
