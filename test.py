import cv2
import numpy
a = numpy.array([[1,2,3],[4,5,6]])
print(a)
image_path = "./bird.png"
image = cv2.imread(image_path)
if image is None:
    print("You have an error in the picture")
    exit()
cv2.imshow("image",image)
k = cv2.waitKey(0)
if k == 27:
    cv2.destroyAllWindows()