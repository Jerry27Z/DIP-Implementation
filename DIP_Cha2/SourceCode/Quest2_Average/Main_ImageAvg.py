#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import numpy as np
import cv2

import NoiseGen
import ImageIO


# 定义图像平均
class ImageAverager: 
    # 定义噪声图像生成器，产生噪声图像
    def __init__(self, dirPath="../../NoisyImage/", avgNum=5): 
        self.__noisyImageGenerator = NoiseGen.NoisyImageGenerator(dirPath)
        self.__avgNum = avgNum

    # 高斯噪声平均
    def gaussianAvg(self, imagePath="../../Resource/Average/NYC.jpg"): 
        # 噪声图像集
        noisyImageSet = self.__noisyImageGenerator\
            .addGaussianNoise(imagePath, imageNum=5)
        # 噪声图像求平均
        avgImage = (noisyImageSet.sum(axis=0) / self.__avgNum).astype(np.uint8)
        # 图像写入文件系统
        ImageIO.ImageWriter(avgImage, "../../Result/Average/avgGaussianImage.jpg").write()
        # 图像展示
        cv2.imshow("Gaussian Noisy-Image Sample", cv2.normalize(noisyImageSet[0], \
                    None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8UC3))
        cv2.imshow("Average Image", avgImage)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    # 泊松噪声平均
    def poissonAvg(self, imagePath="../../Resource/Average/NYC.jpg"): 
        noisyImageSet = self.__noisyImageGenerator\
            .addPoissonNoise(imagePath, imageNum=5)
        avgImage = (noisyImageSet.sum(axis=0) / self.__avgNum).astype(np.uint8)
        ImageIO.ImageWriter(avgImage, "../../Result/Average/avgPoissonImage.jpg").write()
        cv2.imshow("Poisson Noisy-Image Sample", cv2.normalize(noisyImageSet[0], \
                    None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8UC3))
        cv2.imshow("Average Image", avgImage)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    # 椒盐噪声平均
    def s_pAvg(self, imagePath="../../Resource/Average/NYC.jpg"): 
        noisyImageSet = self.__noisyImageGenerator\
            .addS_PNoise(imagePath, imageNum=5)
        avgImage = (noisyImageSet.sum(axis=0) / self.__avgNum).astype(np.uint8)
        ImageIO.ImageWriter(avgImage, "../../Result/Average/avgSalt_PepperImage.jpg").write()
        cv2.imshow("Salt_Pepper Noisy-Image Sample", cv2.normalize(noisyImageSet[0], \
                    None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8UC3))
        cv2.imshow("Average Image", avgImage)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


if __name__ == '__main__': 
    print("Wait a second")
    ImageAverager().gaussianAvg()
    ImageAverager().poissonAvg()
    ImageAverager().s_pAvg()
