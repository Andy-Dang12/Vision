import cv2
import numpy as np


img = cv2.imread('data/noise_n.jpg', 0)


kernel = np.ones((5,5), np.uint8)
img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)


cv2.imshow('fw', img)
cv2.waitKey(0)
