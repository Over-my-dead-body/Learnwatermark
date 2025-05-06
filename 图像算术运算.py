import cv2
import numpy as np
img1_path = './duck.png'
img2_path = './output/save_flipped.png.jpg'
img1 = cv2.imread(img1_path)
img2 = cv2.imread(img2_path)
# 图像混合
alpha = 0.5  # 第一幅图像的权重
beta = 0.5   # 第二幅图像的权重
gamma = 0    # 可选的标量值

result = cv2.addWeighted(img1, alpha, img2, beta, gamma)

cv2.imshow("Result",result)
cv2.waitKey(500)
cv2.destroyAllWindows()