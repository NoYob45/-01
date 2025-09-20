#全局阈值分割+自适应阈值分割【Mean+Gaussian】

import cv2
import matplotlib.pyplot as plt
#载入原图
img_original=cv2.imread('data/Pic_20250919163355647.bmp',0)
#全局阈值分割
retval,img_global=cv2.threshold(img_original,130,255,cv2.THRESH_BINARY)
#自适应阈值分割
img_ada_mean=cv2.adaptiveThreshold(img_original,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,15,3)
img_ada_gaussian=cv2.adaptiveThreshold(img_original,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,15,3)
imgs=[img_original,img_global,img_ada_mean,img_ada_gaussian]
titles=['Original Image','Global Thresholding(130)','Adaptive Mean','Adaptive Guassian',]
#显示图片
for i in range(4):
    plt.subplot(2,2,i+1)
    plt.imshow(imgs[i],'gray')
    plt.title(titles[i])
    plt.xticks([])
    plt.yticks([])
plt.show()


