#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
import cv2
from skimage.util import random_noise
import numpy as np

import ImageIO


# 定义图像噪声生成器
class NoisyImageGenerator: 
    # 初始化噪声图像存放位置
    def __init__(self, dirPath="../../NoisyImage/"): 
        self.__dirPath = dirPath
        if (not os.path.exists(self.__dirPath)): 
            os.mkdir(self.__dirPath)

    # 添加高斯噪声
    def addGaussianNoise(self, path="../../Resource/Average/NYC.jpg", imageNum=1): 
        # 读取图像
        sourImageReader = ImageIO.ImageReader(path)
        destImageWriter = ImageIO.ImageWriter(None, None)
        # 定义噪声图像数组，存储多个噪声图像
        destImageSet = np.zeros(np.append(imageNum, sourImageReader.getShape()))
        for index in range(imageNum): 
            # 图像添加高斯噪声
            gaussianImage = cv2.normalize(random_noise(sourImageReader.getImage(), "gaussian"), 
                                          None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8UC3)
            destImageSet[index] = gaussianImage
            # 图像写入到文件系统
            destImageWriter.setImage(gaussianImage)
            destImageWriter.setPath(self.__dirPath + "NoisyImage" + str(index) + ".jpg")
            destImageWriter.write()
        return destImageSet

    # 添加泊松噪声
    def addPoissonNoise(self, path="../../Resource/Average/NYC.jpg", imageNum=1): 
        sourImageReader = ImageIO.ImageReader(path)
        destImageWriter = ImageIO.ImageWriter(None, None)
        destImageSet = np.zeros(np.append(imageNum, sourImageReader.getShape()))
        for index in range(imageNum): 
            # 图像添加泊松噪声
            poissonImage = cv2.normalize(random_noise(sourImageReader.getImage(), "poisson"), 
                                         None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8UC3)
            destImageSet[index] = poissonImage
            destImageWriter.setImage(poissonImage)
            destImageWriter.setPath(self.__dirPath + "NoisyImage" + str(index) + ".jpg")
            destImageWriter.write()
        return destImageSet

    # 添加椒盐噪声
    def addS_PNoise(self, path="../../Resource/Average/NYC.jpg", imageNum=1): 
        sourImageReader = ImageIO.ImageReader(path)
        destImageWriter = ImageIO.ImageWriter(None, None)
        destImageSet = np.zeros(np.append(imageNum, sourImageReader.getShape()))
        for index in range(imageNum): 
            # 图像添加椒盐噪声
            s_pImage = cv2.normalize(random_noise(sourImageReader.getImage(), "s&p"), 
                                     None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8UC3)
            destImageSet[index] = s_pImage
            destImageWriter.setImage(s_pImage)
            destImageWriter.setPath(self.__dirPath + "NoisyImage" + str(index) + ".jpg")
            destImageWriter.write()
        return destImageSet

    # 清除文件夹中的噪声文件
    def cleanNoisyImage(self): 
        files = os.listdir(self.__dirPath)
        for file in files: 
            filePath = self.__dirPath + file
            if os.path.isfile(filePath and 
                              os.path.splitext(file)[0][:10] == "NoisyImage"): 
                os.remove(filePath)

