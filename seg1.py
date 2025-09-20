import cv2
import numpy as np

AREA_THR  = 100          # 可调
ADAPT_BLK = 61
ADAPT_C   = 5

def area_filter(bin_img, min_area=AREA_THR):
    contours, _ = cv2.findContours(bin_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    big_cnts = [cnt for cnt in contours if cv2.contourArea(cnt) >= min_area]
    mask = np.zeros_like(bin_img)
    cv2.drawContours(mask, big_cnts, -1, 255, -1)
    return mask, big_cnts

def process(bgr):
    gray      = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    # 反色：黑=异物（毛、黑点）
    bin_adapt = cv2.adaptiveThreshold(gray, 255,
                                      cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                      cv2.THRESH_BINARY_INV,  # 关键反转
                                      ADAPT_BLK, ADAPT_C)
    mask, big_cnts = area_filter(bin_adapt)

    bin_white = cv2.bitwise_not(bin_adapt)  # 255↔0

    # 1. 背景
    black_bg = cv2.addWeighted(bgr, 0.6, np.zeros_like(bgr), 0.4, 0)

    # 2. 杂质粗轮廓
    cv2.drawContours(black_bg, big_cnts, -1, (0, 0, 255), 1)

    return gray, bin_adapt, mask, black_bg, len(big_cnts)