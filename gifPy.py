import cv2
import os
# 保存的视频路径及视频size(1000, 1000)
writer = cv2.VideoWriter('apf.mp4', cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), 25, (1000, 1000), True)

# **********设置帧的数量**********
total_frame = len(os.listdir('./result/'))
for frame_num in range(total_frame):
    img_path = './result/test'+str(frame_num)+'.jpg'   #图片路径
    read_img = cv2.imread(img_path)
    writer.write(read_img)
writer.release()

