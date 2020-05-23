#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import cv2


# 图像读取
class ImageReader: 
    def __init__(self, path, mode=cv2.IMREAD_COLOR): 
        self.__path = path
        self.__image = cv2.imread(self.__path, mode)
        self.__shape = self.__image.shape
    
    def getImage(self): 
        return self.__image
    
    def getPath(self): 
        return self.__path
    
    def getShape(self): 
        return self.__shape


# 图像写入
class ImageWriter: 
    def __init__(self, image, path): 
        self.__image = image
        self.__path = path
    
    def write(self): 
        cv2.imwrite(self.__path, self.__image)
    
    def setImage(self, image): 
        self.__image = image
    
    def setPath(self, path): 
        self.__path = path