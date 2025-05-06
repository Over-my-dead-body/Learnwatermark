#打开图片
import os
import cv2
img_path = "./duck.png"
img = cv2.imread(img_path)

#获取和更改图像里某一片内容
roi = img[50:100,50:100]
img[50:100,50:100] = [0,255,0]

#展示图片
cv2.imshow('my image',img)

#访问修改像素
pixel_value = img[98,190]
print(pixel_value)
img[98,190] = [255,255,255]
print(pixel_value)

#分离和合并通道
b,g,r = cv2.split(img)
merged_img = cv2.merge([b,g,r])

key = cv2.waitKey(0)
if key == ord('s'):
    output_path = 'output/output_1.jpg'
    cv2.imwrite(output_path,img)
    #给图片中文名称（直接起中文名乱码）
    target_path = 'output/output_处理基础.jpg'
    if target_path is None:
        os.rename(output_path,target_path)
    else:
        print("error with saving image")
else:
    exit()
cv2.destroyAllWindows()