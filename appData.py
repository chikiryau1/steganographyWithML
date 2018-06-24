def get100BytesMessage():
    message100BytesFile = open('messages/base.txt', 'r')
    message100Bytes = message100BytesFile.read()
    return message100Bytes

def getDiploma():
    diplomaFile = open('DiplomaTex.txt', 'r')
    diplomaText = diplomaFile.read()
    return diplomaText

testImages = {
    'testImages/4.2.03.tiff': 'baboon',
    'testImages/4.2.05.tiff': 'airplane',
    'testImages/4.2.07.tiff': 'peppers',    
    'testImages/2.1.11.tiff': 'earth',    
}

elmData = {
    'baboon': [0.0011260, 0.999999000, 0.9999970, 888.096],
    'airplane': [0.0011150, 0.999999000, 0.9999760, 896.839],
    'peppers': [0.0011560, 0.999999000, 0.9999850, 865.038],
    'earth': [0.0011310, 0.999999000, 0.9999600, 884.137]
}


dataList = ['MSE', 'Corr', 'SSIM', 'fusion']
lsbData = dict.fromkeys(['baboon', 'airplane',  'peppers', 'earth'])
kohonenData = dict.fromkeys(['baboon', 'airplane',  'peppers', 'earth'])