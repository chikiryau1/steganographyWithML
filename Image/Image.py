class Image:

    def __init__(self, path):
        self.path = path
        pass

    def toByteArray(self):
        """
            Method receives a path to image and
            returns its byte representation. 
        """
        pass 
    
    def toImage(self, byteArray, path):
        """
            Method receives a byte representation of image and
            writes it into file.
        """
        pass   

    def divide(self, width, height):
        """
            Method divides an image to blocks with size width*height
            Returns array of blocks.
        """
        pass   

    def joinBlocks(self, arrayOfBlocks):
        """
            Method joins blocks from arrayOfBlocks to array of bytes.
            Returns array of bytes.
        """
        pass 