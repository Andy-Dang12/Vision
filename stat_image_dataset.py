from typing import Iterator
from glob import glob
import posixpath as P
import numpy as np
import cv2
from time import time


class StatImageDataset(object):
    mean_BGR:np.ndarray = None
    mean_RGB:np.ndarray = None
    
    var_BGR:np.ndarray = None
    var_RGB:np.ndarray = None
    
    std_BGR:np.ndarray = None
    std_RGB:np.ndarray = None
    
    num_pixel:int = 0
    
    def __init__(self, imgs:Iterator[str]):
        self.imgs = imgs
        
    @property
    def mean(self):
        if self.mean_BGR is None or self.mean_RGB is None:
            self.cacu_mean_RGB()
        return self.mean_RGB
    
    @property
    def std(self):
        if self.std_BGR is None or self.std_RGB is None:
            self.cacu_std_RGB()
        return self.std_RGB
    
    def cacu_mean_RGB(self) -> np.ndarray:
        tong = np.zeros(3, dtype=np.uint64)
        for imgp in self.imgs:
            img = cv2.imread(imgp)
            hei, wid = img.shape[:2]
            self.num_pixel += hei * wid
            tong += img.sum(axis=(0, 1))
            
        self.mean_BGR = tong / self.num_pixel
        self.mean_RGB = np.flip(self.mean_BGR)
        
        return self.mean_RGB
    
    def cacu_variance_RGB(self) -> np.ndarray:
        if self.mean_BGR is None or self.mean_RGB is None:
            self.cacu_mean_RGB()
        
        total_var = np.zeros(3, dtype=np.float64)
        for imgp in self.imgs:
            img = cv2.imread(imgp)
            square = np.square(img - self.mean_BGR)
            total_var += square.sum((0, 1))
        
        self.var_BGR = total_var / self.num_pixel
        self.var_RGB = np.flip(self.var_BGR)
        
        return self.var_RGB
    
    def cacu_std_RGB(self) -> np.ndarray:
        if self.var_BGR is None or self.var_RGB is None:
            self.cacu_variance_RGB()
        
        self.std_BGR = np.sqrt(self.var_BGR)
        self.std_RGB = np.flip(self.std_BGR)
        return self.std_RGB

if __name__ == "__main__":
    inp = '/home/tz/Downloads/data/14_11/Quan'
    imgs = glob(P.join(inp, '*.jpg'))
    stat = StatImageDataset(imgs)
    
    m = time()
    mean = stat.mean
    mm = time()
    print('mean = ', mean, 'runtime = ', mm-m)
    s = time()
    std = stat.std
    ss = time()
    
    print('std = ', std, 'runtime = ', ss-s)