# -*- coding: cp1251 -*-

import multiprocessing
import os
import time
import numpy as np
import matplotlib.pyplot as plt

import candle
import cv2


def display_img(image1):
    plt.subplots(nrows=1, ncols=1, figsize=(10, 10))
    plt.imshow(image1, cmap='gray')
    plt.axis('off')
    plt.title('Input')
    #plt.subplots(nrows=1, ncols=1, figsize=(10, 10))
    #plt.imshow(image2, cmap='gray')
    #plt.axis('off')
    #plt.title('Input')    
    
    plt.show();

#_______________________________________________________________________________________________________________

image_path = 'F:\Python/candle/mask23.jpg'
image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE) # ���������� cv2.IMREAD_GRAYSCALE, ��� cv2.IMREAD_COLOR ������, ��� skimage
cnts = candle.candle_cnts(image)

cnt = cnts[0]   # <<< �������� � �������

# ������������     //      ������������, ��� ����� multipricessing ������� display_img �������
cv2.drawContours(image, [cnt], -1, (255,0,0), 2)
cv2.imwrite('F:\Python/candle/cndl_nn.jpg', image)
img_cnt = cv2.imread('F:\Python/candle/cndl_nn.jpg')

# ��������� ������
print(len(cnts)) # ����� ����������� ��������
print(len(cnt))  # ����� ����� � ��������� �������
print(cnt)       # ���������� ���������� �������

#___________________________________________________________________________________________________________________

#if __name__ == "__main__":
#    print("starting __main__")
    
#    multiprocessing.Process(target=display_img(img_cnt), args=([1, 2, 3],)).start()
    
#    print("exiting main")
#    os._exit(0) # this exits immediately with no cleanup or buffer flushing