#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import sys
import numpy as np
import cv2
import ImageIO


# 定义图像插值
class Interpolator: 
    
    # 检查原图像与目标图像的深度是否相同
    def checkDepth(self, sourShape, destShape): 
        if (sourShape[2] == destShape[2]): 
            return True
        else: 
            print("The destImage depth is ", str(destShape[2]), 
                  ", while the sourImage depth is ", str(sourShape[2]), 
                  ". Can not interpolate with different depth. ", file=sys.stderr)
            return False
    
    # 检查输入参数是否合理
    def checkArg(self, sourShape, destShape, fraction): 
        # 长宽等比缩放
        if (destShape is None and fraction > 0): 
            legalDestShape = np.array([fraction * sourShape[0], fraction * sourShape[1], sourShape[2]], dtype=int)
        # 任意大小缩放
        elif (fraction <= 0 and destShape is not None and self.checkDepth(sourShape, destShape)): 
            legalDestShape = destShape
        else: 
            print("Argument Error!", file=sys.stderr)
            sys.exit()
        return legalDestShape
    
    # 边界填充。mode 0：用0填充；mode 1：边界重复填充
    def padding(self, sourImage, pixelNum=1, mode=0): 
        sourShape = sourImage.shape
        destImage = np.zeros([sourShape[0] + 2 * pixelNum, sourShape[1] + 2 * pixelNum, 
                              sourShape[2]])
        destImage[pixelNum: pixelNum + sourShape[0], pixelNum: pixelNum + sourShape[1]] = sourImage
        if (mode != 0): 
            for col in range(pixelNum): 
                destImage[:, col] = destImage[:, pixelNum]
                destImage[:, col + sourShape[1] + pixelNum] = destImage[:, sourShape[1] + pixelNum - 1]
            for row in range(pixelNum): 
                destImage[row] = destImage[pixelNum]
                destImage[row + sourShape[0] + pixelNum] = destImage[sourShape[0] + pixelNum - 1]
        return destImage
    
    # Nearest-Neighbor最近邻插值
    def nearest_neighborInterpolation(self, sourImage, destShape=None, fraction=-1): 
        sourShape = sourImage.shape
        # 检查输入参数
        destShape = self.checkArg(sourShape, destShape, fraction)
        
        destImage = np.zeros(destShape, dtype=np.uint8)
        for rowNum in range(destShape[0]): 
            # 映射到原图像的位置
            sourRowNum = int(rowNum / destShape[0] * (sourShape[0] - 1) - 0.5) + 1

            for colNum in range(destShape[1]):
                sourColNum = int(colNum / destShape[1] * (sourShape[1] - 1) - 0.5) + 1

                # 最近邻
                destImage[rowNum, colNum] = sourImage[sourRowNum, sourColNum]
        return destImage
    
    # Bi-Linear双线性插值
    def bi_linearInterpolation(self, sourImage, destShape=None, fraction=-1, mode=0): 
        sourShape = sourImage.shape
        destShape = self.checkArg(sourShape, destShape, fraction)
        destImage = np.zeros(destShape)
        
        # 设置填充行、列数为1
        paddingPixel = 1
        paddingImage = self.padding(sourImage, paddingPixel, mode)
        
        for rowNum in range(destShape[0]): 
            # 映射到填充图像的位置
            paddingRowNum = rowNum / destShape[0] * (sourShape[0] - 1) + paddingPixel
            # 最近下界位置
            i_paddingRowNum = int(paddingRowNum)
            # 小数部分
            f_rowFrac = paddingRowNum - i_paddingRowNum # v

            # 当前行
            paddingImageThisRow = paddingImage[i_paddingRowNum]
            # 下一行
            paddingImageNextRow = paddingImage[i_paddingRowNum + 1]

            for colNum in range(destShape[1]):
                paddingColNum = colNum / destShape[1] * (sourShape[1] - 1) + paddingPixel
                i_paddingColNum = int(paddingColNum)
                f_colFrac = paddingColNum - i_paddingColNum # u

                # 计算缩放图像的像素值
                destImage[rowNum, colNum] = ((1 - f_colFrac) * (1 - f_rowFrac) * paddingImageThisRow[i_paddingColNum] 
                                             + (1 - f_colFrac) * f_rowFrac * paddingImageNextRow[i_paddingColNum] 
                                             + (1 - f_rowFrac) * f_colFrac * paddingImageThisRow[i_paddingColNum + 1] 
                                             + f_rowFrac * f_colFrac * paddingImageNextRow[i_paddingColNum + 1])
        # 限制缩放图像的像素值在0-255之间
        destImage = np.clip(destImage, 0, 255).astype(np.uint8)
        return destImage
    
    # 计算三次多项式
    def triplePoly(self, inputNum, a=-0.5): 
        absInput = abs(inputNum)
        if (0 <= absInput < 1): 
            return (1 - (a + 3) * pow(absInput, 2) + (a + 2) * pow(absInput, 3))
        elif (1 <= absInput < 2): 
            return (-4 * a + 8 * a * absInput - 5 * a * pow(absInput, 2) + a * pow(absInput, 3))
        else: 
            return 0

    # Bi-Cubic双三次插值
    def bi_cubicInterpolation(self, sourImage, destShape=None, fraction=-1, mode=0): 
        sourShape = sourImage.shape
        destShape = self.checkArg(sourShape, destShape, fraction)
        destImage = np.zeros(destShape)

        # 设置填充行、列数为2
        paddingPixel = 2
        paddingImage = self.padding(sourImage, paddingPixel, mode)
        
        # 映射到填充图像的位置矩阵
        posArray = np.zeros([4, 4, sourShape[2]], dtype=np.uint8)
        for rowNum in range(destShape[0]): 
            paddingRowNum = rowNum / (destShape[0] - 1) * (sourShape[0] - 1) + paddingPixel
            i_paddingRowNum = int(paddingRowNum)
            f_rowFrac = paddingRowNum - i_paddingRowNum # v

            # 上一行
            prevRowIndex = i_paddingRowNum - 1
            # 下下行
            n_NextRowIndex = i_paddingRowNum + 2

            # 行三次多项式计算结果
            triplePolyRowArray = np.array([self.triplePoly(1 + f_rowFrac), 
                                        self.triplePoly(f_rowFrac), 
                                        self.triplePoly(1 - f_rowFrac), 
                                        self.triplePoly(2 - f_rowFrac)])

            for colNum in range(destShape[1]): 
                paddingColNum = colNum / (destShape[1] - 1) * (sourShape[1] - 1) + paddingPixel
                i_paddingColNum = int(paddingColNum)
                f_colFrac = paddingColNum - i_paddingColNum # u

                prevColIndex = i_paddingColNum - 1
                n_NextColIndex = i_paddingColNum + 2

                posArray = paddingImage[prevRowIndex: n_NextRowIndex+1, prevColIndex: n_NextColIndex+1]

                # 列三次多项式计算结果
                triplePolyColArray = np.array([self.triplePoly(1 + f_colFrac), 
                                            self.triplePoly(f_colFrac), 
                                            self.triplePoly(1 - f_colFrac), 
                                            self.triplePoly(2 - f_colFrac)]).T
                # 计算缩放图像每一个通道的像素值
                for channel in range(posArray.shape[2]): 
                    destImage[rowNum, colNum, channel] = triplePolyRowArray.dot(posArray[:, :, channel])\
                    .dot(triplePolyColArray)
        destImage = np.clip(destImage, 0, 255).astype(np.uint8)
        return destImage


if __name__ == '__main__': 
    sourImageReader = ImageIO.ImageReader("../../Resource/Interpolation/bdd_xrr.png")
    print("Input scale times: ", end='')
    times = float(input())
    
    print("Wait a second")
    nnIImage = Interpolator().nearest_neighborInterpolation(sourImageReader.getImage(), fraction=times)
    blIImage = Interpolator().bi_linearInterpolation(sourImageReader.getImage(), fraction=times)
    bcIImage = Interpolator().bi_cubicInterpolation(sourImageReader.getImage(), fraction=times)
    # 缩放图像写入文件系统
    ImageIO.ImageWriter(nnIImage, "../../Result/Interpolation/destImage_NearNei.png").write()
    ImageIO.ImageWriter(blIImage, "../../Result/Interpolation/destImage_BiLinear.png").write()
    ImageIO.ImageWriter(bcIImage, "../../Result/Interpolation/destImage_BiCubic.png").write()
    print("Results are stored in Result Folder")
    
    # 缩放图像展示
    cv2.imshow("Original Image", sourImageReader.getImage())
    cv2.imshow("Nearest Neighbor Interpolation", nnIImage)
    cv2.imshow("Bi-Linear Interpolation", blIImage)
    cv2.imshow("Bi-Cubic Interpolation", bcIImage)
    
    cv2.waitKey(0)
