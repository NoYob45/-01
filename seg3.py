#大津阈值分割，效果差

import cv2
import matplotlib.pyplot as plt

# 1. 读图
img_original = cv2.imread('data/Pic_20250919163355647.bmp', 0)

# 2. 可选：高斯滤波（去噪，Otsu 更稳）
img_blur = cv2.GaussianBlur(img_original, (13, 13), 13)

# 3. 大津阈值（自动计算最优阈值）
_, img_otsu = cv2.threshold(img_blur, 0, 255,
                            cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# 4. 显示
plt.imshow(img_otsu, 'gray')
plt.title('Otsu Threshold')
plt.xticks([]); plt.yticks([])
plt.show()