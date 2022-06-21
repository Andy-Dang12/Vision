# https://colab.research.google.com/drive/1xV-3hlLQgond2TBEwJSxPyWTXXHMgWFJ?usp=sharing
# https://viblo.asia/p/image-stitching-thuat-toan-dang-sau-cong-nghe-anh-panorama-LzD5dee4KjY
# https://stackoverflow.com/questions/31998428/opencv-python-equalizehist-colored-image

import cv2
import numpy as np


def histogram_equalization(rgb_img:np.ndarray) -> np.ndarray:
    ycrcb_img = cv2.cvtColor(rgb_img, cv2.COLOR_BGR2YCrCb)

    # equalize the histogram of the Y channel
    ycrcb_img[:, :, 0] = cv2.equalizeHist(ycrcb_img[:, :, 0])
    equalized_img = cv2.cvtColor(ycrcb_img, cv2.COLOR_YCrCb2BGR)
    return equalized_img


def histogram_equalization(img:np.ndarray) -> np.ndarray:
    img_yuv = cv2.cvtColor(img,cv2.COLOR_BGR2YUV)
    img_yuv[:,:,0] = cv2.equalizeHist(img_yuv[:,:,0])
    hist_eq = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR)
    return hist_eq


img1 = cv2.imread('data/foto1A.jpg')
img2 = cv2.imread('data/foto1B.jpg')

gray1 = cv2.cvtColor(img1, cv2.COLOR_RGB2GRAY)
gray2 = cv2.cvtColor(img2, cv2.COLOR_RGB2GRAY)
img1 = histogram_equalization(img1)
img2 = histogram_equalization(img2)

#NOTE 1. Key points detection - Feature extractor
# SIFT - Scale Invariant Feature Transform
# AKAZE, SUFT, ORB các Feature extractor khác có thể sử dụng
SIFT_detector = cv2.xfeatures2d.SIFT_create()
kp1, des1 = SIFT_detector.detectAndCompute(gray1, None)
kp2, des2 = SIFT_detector.detectAndCompute(gray2, None)



#NOTE 2. Key points maching
# FLANN maching hoặc Bruce Force Maching
bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=False)
matches = bf.match(des1, des2)
matches = sorted(matches, key= lambda x:x.distance)
matches = matches[:100]

list_kp1 = [kp1[mat.queryIdx].pt for mat in matches]
list_kp2 = [kp2[mat.trainIdx].pt for mat in matches]



#NOTE 3. Perspectivate transform - estimate homography matrix
# Estimate homography matrix with RANSAC.
H, status = cv2.findHomography(np.float32(list_kp1), 
                               np.float32(list_kp2), cv2.RANSAC)

h1, w1, c1 = img1.shape
h2, w2, c2 = img2.shape
result = cv2.warpPerspective(img1, H, (w1+w2, h1))
result[0:h2, 0:w2] = img2
cv2.imshow('dwfa',result)
cv2.waitKey(0)

# using opencv Stitcher_create
# stitcher = cv2.Stitcher_create()
# status, stitched = stitcher.stitch([img1, img2])
# if status == 0:
# 	cv2.imshow('dw',stitched)
# 	cv2.waitKey(0)
