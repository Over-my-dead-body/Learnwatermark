import cv2

def resize_photo(initImage,targetImage):
    initShape = initImage.shape
    initShapeYX = (initShape[0],initShape[0])
    targetShape = targetImage.shape
    targetShapeYX = (targetShape[0],targetShape[1])
    resizedImage = cv2.copyMakeBorder(initImage,0,targetShapeYX[0]-initShapeYX[1],0,targetShapeYX[1]-initShapeYX[1],borderType=cv2.BORDER_REFLECT)
    return resizedImage
def resize_photo1(initImage,targetImage):
    # 获取目标图像的尺寸（假设targetImage是载体图像的一个通道，shape为 (h, w)）
    target_h, target_w = targetImage.shape[:2]
    # 获取初始图像的尺寸
    init_h, init_w = initImage.shape[:2]
    # 计算需要填充的高度和宽度
    pad_h = max(target_h - init_h, 0)
    pad_w = max(target_w - init_w, 0)
    # 使用反射填充（若目标尺寸更大则填充，否则裁剪）
    resized = cv2.copyMakeBorder(
        initImage,
        top=0,
        bottom=pad_h,
        left=0,
        right=pad_w,
        borderType=cv2.BORDER_REFLECT
    )
    # 确保最终尺寸与目标一致（若目标更小则裁剪）
    resized = resized[:target_h, :target_w]
    return resized

img1 = cv2.imread('./bird.png')
target_img = cv2.imread('./duck.png')
shape = target_img.shape # 获取图片大小
shape1 = (shape[0],shape[1])
shape = img1.shape
shape2 = (shape[0],shape[1])
print(shape)
# 边填黑，注意yx反
resized = cv2.copyMakeBorder(img1, 0,shape1[0]-shape2[0], 0, shape1[1]-shape2[0], borderType=cv2.BORDER_CONSTANT,value=0)


cv2.imshow('before',img1)
cv2.imshow('after',resize_photo1(img1,target_img))
print(resize_photo1(img1,target_img).shape,resize_photo(img1,target_img).shape)
# 调整图片大小成功
cv2.waitKey(0)