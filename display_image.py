import cv2
image_path = "./bird.png"

#cv2.imread() 读取图像文件，返回一个 NumPy 数组。
#如果图像路径错误或文件不存在，返回 None。
image = cv2.imread(image_path)
if image is None:
    print("error")
    exit()
cv2.imshow("display image",image)

# 参数 0 表示无限等待，直到用户按下任意键
key = cv2.waitKey(0)
if key == ord('s'):
    output_path = ('save_image.pdf')
    cv2.imwrite(output_path,image)
    print(f'photo saved in {output_path}')
elif key == ord('q'):
    print("now exit")
    exit()
else:
    print("no photo saved")
cv2.destroyAllWindows()