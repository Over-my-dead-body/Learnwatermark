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
def resize_photo(initImage, targetImage, border_type=cv2.BORDER_REFLECT, value=0):
    target_h, target_w = targetImage.shape[:2]
    init_h, init_w = initImage.shape[:2]
    pad_h = max(target_h - init_h, 0)
    pad_w = max(target_w - init_w, 0)
    resized = cv2.copyMakeBorder(
        initImage, 0, pad_h, 0, pad_w,
        borderType=border_type,
        value=value
    )
    return resized[:target_h, :target_w]

def encode_watermark(bed, wat, Layers, way):
    if way == 1:
        wat = resize_photo(wat, bed, cv2.BORDER_CONSTANT, 0)
    elif way == 2:
        wat = resize_photo(wat, bed, cv2.BORDER_REFLECT)
    else:
        raise ValueError("way参数必须为1或2")
    bed = bed.copy()
    height, width = bed.shape[:2]
    for i in range(height):
        for j in range(width):
            w = bed[i][j] // (2 ** Layers)
            if w % 2 == 0 and wat[i][j] == 1:
                new_val = bed[i][j] + (2 ** Layers)
                bed[i][j] = min(new_val, 255)
            elif w % 2 == 1 and wat[i][j] == 0:
                new_val = bed[i][j] - (2 ** Layers)
                bed[i][j] = max(new_val, 0)
    return bed
def decode_watermark(bed, Layers):
    height, width = bed.shape[:2]
    wat = np.zeros((height, width), dtype=np.uint8)
    for i in range(height):
        for j in range(width):
            w = bed[i][j] // (2 ** Layers)
            wat[i][j] = 1 if (w % 2 == 1) else 0
    return wat

# 读取并二值化水印图像
watermarkImage = cv2.imread('./img_test1.jpg', cv2.IMREAD_GRAYSCALE)
_, watermarkImage = cv2.threshold(watermarkImage, 127, 1, cv2.THRESH_BINARY)

# 用户输入
Layers = int(input("水印添加层数（0-7）"))
watermarkWay = int(input("1=单水印，2=反射水印"))


# 创建 VideoCapture 对象，读取视频文件
cap = cv2.VideoCapture('example.mp4')
# 检查视频是否成功打开
if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

# 获取视频的帧率和尺寸
fps = int(cap.get(cv2.CAP_PROP_FPS))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# 创建 VideoWriter 对象，保存处理后的视频
fourcc = cv2.VideoWriter_fourcc(*'H264')
out = cv2.VideoWriter('output.mp4',fourcc,fps,(width,height),isColor=True)

# 读取视频帧
while True:
    ret, frame = cap.read()
    # 如果读取到最后一帧，退出循环
    if not ret:
        break

    #帧作为水印载体,提取当前帧的RGB通道（OpenCV默认BGR格式）
    bb, gb, rb = cv2.split(frame)

    # 调整水印尺寸与当前帧匹配
    wat_resized = resize_photoBORDER_CONSTANT(watermarkImage, bb) if watermarkWay == 1 else resize_photoBORDER_REFLECT(watermarkImage, bb)

    # 嵌入水印
    encoded_b = encode_watermark(bb, watermarkImage, Layers, watermarkWay)
    encoded_g = encode_watermark(gb, watermarkImage, Layers, watermarkWay)
    encoded_r = encode_watermark(rb, watermarkImage, Layers, watermarkWay)

    # 合并回 BGR 格式
    encoded_frame_bgr = cv2.merge([encoded_b, encoded_g, encoded_r])

    # 写入输出视频
    out.write(encoded_frame_bgr)

    # 提取水印
    bo, go, ro = cv2.split(encoded_frame_bgr)
    decoded_b = decode_watermark(bo, Layers)
    decoded_g = decode_watermark(go, Layers)
    decoded_r = decode_watermark(ro, Layers)
    decoded_watermark = cv2.merge([decoded_b, decoded_g, decoded_r])
    cv2.imshow('Decoded Watermark', decoded_watermark * 255)  # 二值图转0-255显示

# 释放资源
cap.release()
out.release()
cv2.destroyAllWindows()
