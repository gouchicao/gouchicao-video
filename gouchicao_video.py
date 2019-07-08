import argparse
import os
import time
import sys
import cv2
import numpy as np

import darknet_model_client as dm_client
from random import randint


WINDOW_NAME = 'gouchicao video'


client = None
class_colors = {}     #每个类别对应的标记颜色
image_exts = ['jpg', 'png', 'jpeg']


def run(video_file, time_delay):
    cap = cv2.VideoCapture(video_file)
    if not cap.isOpened():
        print('video [{}] is not open'.format(video_file))
        sys.exit()

    tracker = None
    fps = None
    while True:
        ok, frame = cap.read()
        if not ok:
            break

        if not video_file:
            frame = cv2.flip(frame, 1, 0)

        recognition(frame)

        cv2.imshow(WINDOW_NAME, frame)

        key_code = cv2.waitKey(time_delay)
        if key_code == ord('q') or key_code == 27: #q or esc
            sys.exit()

    cap.release()
    cv2.destroyAllWindows()


def recognition(frame):
    timer = cv2.getTickCount()
    
    image_data = cv2.imencode('.jpg', frame)[1].tobytes()
    response = client.detect(image_data)

    if response:
        for object in response.object:
            class_name = object.name
            class_color = get_class_color(class_name)
            
            rect = object.rectangle
            cv2.rectangle(frame, (rect.x, rect.y), (rect.x+rect.w, rect.y+rect.h), class_color, 2)
            cv2.putText(frame, class_name, (rect.x, rect.y), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255,125,0), 2, lineType=cv2.LINE_AA)
        
        fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)
        cv2.putText(frame, "FPS : " + str(int(fps)), (20,40), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2)


def get_class_color(class_name):
    if class_name not in class_colors:
        class_colors[class_name] = np.random.uniform(0, 255, size=(3))
    return class_colors[class_name]


def get_ext_name(filename):
    ext_name = os.path.splitext(filename)[1]
    if ext_name: #May not have an extension
        ext_name = ext_name[1:] #remove.
        ext_name = ext_name.lower()

    return ext_name


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--server_address', type=str, help='server address 127.0.0.1:7713', default='[::]:7713')
    parser.add_argument('-v', '--video', type=str, help='video file path. default open camera.')
    parser.add_argument('-f', '--image_file', type=str, help='image file path.')
    parser.add_argument('-d', '--image_directory', type=str, help='image directory.')
    parser.add_argument('-t', '--time_delay', type=int, help='The time delay between frames and frames, in milliseconds. Set to 0, pause, then press any key to continue displaying.', default=1)

    args = parser.parse_args()

    client = dm_client.gRPCClient(args.server_address)
    time_delay = args.time_delay

    image_files = []
    if args.image_file:
        image_files.append(args.image_file)

    if args.image_directory:
        for parent, dirnames, filenames in os.walk(args.image_directory):
            for filename in filenames:
                ext_name = get_ext_name(filename)
                if ext_name in image_exts:
                    image_files.append(os.path.join(parent, filename))

    if image_files:
        # 如果只有一张图片且没有设置time_delay值，那么就设置为0。代表等待按任意键继续。
        if len(image_files) == 1 and time_delay == 1:
            time_delay = 0

        for image_file in image_files:
            run(image_file, time_delay)
    else:
        video_file = args.video
        if not video_file:
            video_file = 0
        run(video_file, time_delay)
