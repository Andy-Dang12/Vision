from base64 import b64decode, b64encode
from typing import overload
from PIL import Image, ImageFile
from io import BytesIO
from os.path import isfile

class Ecryption_Image(object):

    @staticmethod
    def encode(image:Image) -> str:
        buffered = BytesIO()
        image.save(buffered, format="JPEG")
        return b64encode(buffered.getvalue())

    @overload
    @staticmethod
    def encode(image:str) -> str:
        if not isfile(image):
            raise Exception("cannot found image at " + image)
        
        with open(image, "rb") as f:
            converted_string = b64encode(f.read())
        return converted_string

    @staticmethod
    def decode(encoded_str:str) -> ImageFile.ImageFile:
        return Image.open(BytesIO(b64decode(encoded_str)))

