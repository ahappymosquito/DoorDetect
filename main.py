import cv2
import numpy as np
from pynput import *

video = cv2.VideoCapture(0)
video.set(cv2.CAP_PROP_FPS,30)
video.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
video.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

control = keyboard.Controller()

# fps = video.get(cv2.CAP_PROP_FPS)
# print(fps)
# size = (int(video.get(cv2.CAP_PROP_FRAME_WIDTH)), int(video.get(cv2.CAP_PROP_FRAME_HEIGHT)))
# print(size)

# 门框位置
# x, y, w, h = 1370, 400, 200, 300
# specified_region = frame[y:y + h, x:x + w]


def calculate_dark_color_pixel_count(region, color):
    bgr_color = np.array([int(color[5:7], 16), int(color[3:5], 16), int(color[1:3], 16)], dtype=np.uint8)
    dark_pixels = np.count_nonzero(np.all(region < bgr_color, axis=-1))
    return dark_pixels

while True:
    ret, frame = video.read()

    roi_x, roi_y, roi_w, roi_h = 1460, 440, 10, 50
    roi_region = frame[roi_y:roi_y + roi_h, roi_x:roi_x + roi_w]

    color_code = '#222b36'
    dark_color_pixels = calculate_dark_color_pixel_count(roi_region, color_code)
    total_pixels = roi_w * roi_h

    black_ratio = dark_color_pixels / total_pixels

    if black_ratio > 0.8:
        cv2.putText(frame, "Warning!", (roi_x, roi_y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
        with control.pressed(keyboard.Key.alt_l , keyboard.Key.tab):
            pass
        break
        # print("hello world")
    # cv2.rectangle(frame, (roi_x, roi_y), (roi_x + roi_w, roi_y + roi_h), (0, 255, 0), 2)
    # cv2.imshow("video", frame)

    # cv2.imshow("roi",roi_region)

    c = cv2.waitKey(1)
    if c == 27:
        break

video.release()
cv2.destroyAllWindows()
