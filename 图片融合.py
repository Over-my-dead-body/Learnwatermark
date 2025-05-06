import cv2
import numpy as np
def resize_photoBORDER_REFLECT(initImage,targetImage):
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
def resize_photoBORDER_CONSTANT(initImage,targetImage):
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
        borderType=cv2.BORDER_CONSTANT,
        value=0
    )
    # 确保最终尺寸与目标一致（若目标更小则裁剪）
    resized = resized[:target_h, :target_w]
    return resized
def encode_watermark(bed,wat,Layers,way):
    if way == 1:
        wat = resize_photoBORDER_CONSTANT(wat,bed)
    elif way ==2:
        wat = resize_photoBORDER_REFLECT(wat,bed)
    bed = bed.copy()  # 避免修改原数组
    bedX = len(bed)
    bedY = len(bed[0])
    for i in range(0,bedX):
        for j in range(0,bedY):
            w = bed[i][j] // (2 ** Layers)
            if w % 2 == 0 and wat[i][j] == 1:
                new_val = bed[i][j] + (2 ** Layers)
                bed[i][j] = min(new_val, 255)  # 限制上限
            elif w % 2 == 1 and wat[i][j] ==0:
                new_val = bed[i][j] - (2 ** Layers)
                bed[i][j] = max(new_val, 0)    # 限制下限
    return bed
def decode_watermark(bed,Layers):
    bedX = len(bed)
    bedY = len(bed[0])
    wat = np.zeros((bedX,bedY),dtype=np.uint8)
    for i in range(0,bedX):
        for j in range(0,bedY):
            w = bed[i][j] // (2 ** Layers)
            if w % 2 == 1:
                wat[i][j] = 1
    return wat

bedrockImage = cv2.imread('./duck.png')
watermarkImage = cv2.imread('./img_test1.jpg')
bb,gb,rb = cv2.split(bedrockImage)
bw,gw,rw = cv2.split(watermarkImage)

Layers = int(input("水印添加层数（0-7）"))# 255->二进制8位 故有8层，表示为0-7
watermarkWay = int(input("1=单水印，2=反射水印"))# 两种水印生成方式选择
encoedImage = cv2.merge([encode_watermark(bb,bw,Layers,watermarkWay),encode_watermark(gb,gw,Layers,watermarkWay),encode_watermark(rb,rw,Layers,watermarkWay)])

cv2.imwrite('/output/save_watermark.png',encoedImage)

bo,go,ro = cv2.split(encoedImage)
decodeImage = cv2.merge([decode_watermark(bo,Layers),decode_watermark(go,Layers),decode_watermark(ro,Layers)])

cv2.imshow('before',bedrockImage)
cv2.imshow('after',encoedImage)
cv2.imshow('water',decodeImage)
cv2.waitKey(0)
'''
for i in range(a):
    for j in range(b):
        w = Carrier_array[i][j] // (2 ** Layers)
        if w % 2 == 0 and WaterMark_array[i][j] == 1:
            Carrier_array[i][j] = Carrier_array[i][j] + (2 ** Layers)
        elif w % 2 == 1 and WaterMark_array[i][j] == 0:
            Carrier_array[i][j] = Carrier_array[i][j] - (2 ** Layers)
'''