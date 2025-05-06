import cv2
img_path = './.png'
img = cv2.imread(img_path)


# 访问像素值
# img[y, x] 来访问位于 (x, y) 位置的像素值
pixel_value = img[100,200]#访问（200，100）位置
print(pixel_value)#返回的是（B,G,R）信息，与rgb反着
# 彩色图像，可以通过 img[y, x, c] 来访问特定通道 c 的像素值，
# 其中 c 为 0（蓝色）、1（绿色）或 2（红色）
pixel_value = img[100,200,0]#访问的（200，100）处蓝色值
print(pixel_value)

#修改像素值


# 图像翻转
flipped_img = cv2.flip(img, 1)  # 水平翻转
cv2.imshow('display image',flipped_img)
cv2.imwrite("output/save_flipped.png",flipped_img)
cv2.waitKey(5000)
cv2.destroyAllWindows()