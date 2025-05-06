import cv2
def zero_end(n):# 最后一位变成0
    return n & (~1)

def oneway_change(b):
    for i in range(0, 720):
        for j in range(0, 930):
            b[i][j] = zero_end(b[i][j])
    return b

img = cv2.imread('./duck.png')
cv2.imshow('before',img)
b,g,r = cv2.split(img)
print(b)

print(len(b),len(b[0]))
# b = [ [,,930元素],
#       [],
#       []
#     720元素]
print(oneway_change(b))
# 完美实现更改最低位的效果咯
merged_img = cv2.merge([oneway_change(b),oneway_change(g),oneway_change(r)])
cv2.imshow('after',merged_img)
cv2.waitKey(0)