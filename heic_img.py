import cv2
import numpy as np
import pyheif
from PIL import Image

def read_heic_as_cv2_image(path):
    # Đọc tệp HEIC
    heif_file = pyheif.read(path)

    # Chuyển đổi sang PIL Image
    image = Image.frombytes(
        heif_file.mode,
        heif_file.size,
        heif_file.data,
        "raw",
        heif_file.mode,
        heif_file.stride,
    )

    # Chuyển đổi sang OpenCV Image
    open_cv_image = np.array(image)
    # Chuyển từ RGB (Pillow) sang BGR (OpenCV)
    open_cv_image = open_cv_image[:, :, ::-1].copy()
    return open_cv_image

def resize_image(image, width):
    # Tính tỷ lệ và resize ảnh
    ratio = width / image.shape[1]
    dim = (width, int(image.shape[0] * ratio))
    return cv2.resize(image, dim, interpolation=cv2.INTER_AREA)

def merge_images(image1, image2):
    # Đảm bảo cùng chiều rộng
    if image1.shape[1] > image2.shape[1]:
        image2 = resize_image(image2, image1.shape[1])
    elif image1.shape[1] < image2.shape[1]:
        image1 = resize_image(image1, image2.shape[1])

    # Ghép hai ảnh theo chiều dọc
    return cv2.vconcat([image1, image2])


cv_image1 = read_heic_as_cv2_image('IMG_2234.HEIC')
cv_image2 = read_heic_as_cv2_image('IMG_2235.HEIC')


merged_image = merge_images(cv_image1, cv_image2)

# Lưu ảnh kết quả
cv2.imwrite('output.png', merged_image, [cv2.IMWRITE_PNG_COMPRESSION, 0])
