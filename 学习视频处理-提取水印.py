import cv2
import numpy as np

# 水印提取函数（与你原有代码一致）
def decode_watermark(bed, Layers):
    height, width = bed.shape[:2]
    wat = np.zeros((height, width), dtype=np.uint8)
    for i in range(height):
        for j in range(width):
            w = bed[i][j] // (2 ** Layers)
            wat[i][j] = 1 if (w % 2 == 1) else 0
    return wat

# 用户输入：使用的水印层数（必须与嵌入时一致）
Layers = int(input("请输入嵌入水印时使用的层数（0-7）："))

# 打开视频文件
cap = cv2.VideoCapture('output.mp4')  # 替换为你自己的输出视频路径
if not cap.isOpened():
    print("Error: 无法打开视频文件")
    exit()

# 创建一个窗口用于实时显示提取出的水印
cv2.namedWindow('Extracted Watermark', cv2.WINDOW_NORMAL)

frame_count = 0
skip_frame = 5  # 可选：每隔几帧提取一次水印，避免重复

while True:
    ret, frame = cap.read()
    if not ret:
        break

    b, g, r = cv2.split(frame)

    # 只提取一个通道的水印
    wat = decode_watermark(b, Layers)

    # 显示或保存
    cv2.imshow('Watermark', wat * 255)
    cv2.imwrite(f'output/watermark_frame_{frame_count}.png', wat * 255)


    frame_count += 1

cap.release()
cv2.destroyAllWindows()
