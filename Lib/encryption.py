from base64 import b64decode, b64encode
from typing import overload
from PIL import Image, ImageFile
from io import BytesIO
from os.path import isfile
import cv2
import numpy as np


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


# https://jdhao.github.io/2020/03/17/base64_opencv_pil_image_conversion/
def encode_pil(image:Image) -> str:
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    return b64encode(buffered.getvalue())


def decode_pil(encoded_str:str) -> ImageFile.ImageFile:
    return Image.open(BytesIO(b64decode(encoded_str)))


def encode_cv2(image:cv2.Mat) -> str:
    retval, buffer = cv2.imencode('.jpg', image)
    return b64encode(buffer)


def decode_cv2(encoded_str:str) -> cv2.Mat:
    im_bytes = b64decode(encoded_str)
    im_arr = np.frombuffer(im_bytes, dtype=np.uint8)    # im_arr is one-dim Numpy array
    return cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)


if __name__ == '__main__':
    imgp = '/home/tz/Documents/Pytorch_Retinaface/data/widerface/val/images/6--Funeral/6_Funeral_Funeral_6_627.jpg'
    
    def test_base64_cv2(imgp:str=imgp):
        cv = cv2.imread(imgp)
        cv2.imshow('cv2_ori', cv)
        cv2.waitKey(0)
        cv2_str = encode_cv2(cv)
        imgcv = decode_cv2(cv2_str)
        cv2.imshow('cv2_decode', imgcv)
        cv2.waitKey(0)
    
    def test_base64_pil(imgp:str=imgp):
        pil = Image.open(imgp)
        pil.show(title='pil_ori')
        pil_str = encode_pil(pil)
        img = decode_pil(pil_str)
        img.show(title='pil_decode')
    
    test_base64_cv2()
    test_base64_pil()
