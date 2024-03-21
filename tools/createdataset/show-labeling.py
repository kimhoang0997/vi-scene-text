#!/usr/bin/env python

import sys
sys.path.append('/Users/hoangnguyen/GitHub/vi-scene-text')

import argparse, cv2, glob, os, math
import numpy as np
from paddleocr import PaddleOCR
from tools.infer.utility import get_rotate_crop_image,draw_ocr_box_txt
from PIL import Image, ImageDraw, ImageFont


def create_label(filename, tag):
    print(f"Created label for {filename}")

def remove_label(filename):
    print(f"Created label of {filename}")

def cv2_img_add_text(img, text, left_corner: (int, int),
                     text_rgb_color=(255, 255, 255), text_size=12, font='./arial.ttf', **option):
    """
    USAGE:
        cv2_img_add_text(img, '中文', (0, 0), text_rgb_color=(0, 255, 0), text_size=12, font='mingliu.ttc')
    """
    pil_img = img
    if isinstance(pil_img, np.ndarray):
        pil_img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(pil_img)
    font_text = ImageFont.truetype(font=font, size=text_size, encoding=option.get('encoding', 'utf-8'))
    draw.text(left_corner, text, text_rgb_color, font=font_text)
    cv2_img = cv2.cvtColor(np.asarray(pil_img), cv2.COLOR_RGB2BGR)
    return cv2_img


def take_rois_texts(label_path):
    with open(label_path,'r',encoding='utf-8') as label_file:
        lines = label_file.readlines()
        rois = []
        texts = []
        for line in lines:
            coords = line.strip().split(",")
            roi = [[int(coords[0]),int(coords[1])],[int(coords[2]),int(coords[3])],[int(coords[4]),int(coords[5])],[int(coords[6]),int(coords[7])]]
            text = coords[-1]
            rois.append(roi)
            texts.append(text)

    return rois,texts

# Debugger for tag from ocr.ocr
def debugger(filename, image, rois,texts, watch, rate, index):
    font = cv2.FONT_HERSHEY_SIMPLEX
    green = (80, 220, 60)
    yellow = (255, 0, 0)
    img = cv2.resize(image, None, fx=rate, fy=rate)
    font_size = img.shape[1]//50
    drop_score = 0.5
    font_path = "dataset/fonts/arial.ttf"

    image = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    draw_img = draw_ocr_box_txt(
                    image,
                    np.array(rois),
                    texts,
                    font_path=font_path)

    cv2.imshow("Debugger", draw_img)

    while True:
        key = cv2.waitKey(1) & 0xFF if watch else cv2.waitKey(0) & 0xFF
        if key == ord("q"):
            quit()
        elif key == ord('c'):
            cv2.imwrite(filename, image)
        elif key == ord('x'):
            cv2.imwrite(filename, image)
            create_label(filename, rois)
        elif key == ord('e'):
            os.system("rm -f " + filename)
            remove_label(filename)
        elif key == ord('a'):
            return index - 1 if index > 0 else index
        elif key == ord('d'):
            return index + 1


def argument_parser():
    parser = argparse.ArgumentParser(description='Detector with paddleocr knowledge for image datasets')
    parser.add_argument('image_folder', help='the image folder for processing')
    parser.add_argument('labels_path', help='the label path for processing')
    parser.add_argument('-w', '--watch', dest='watch', help='set watch mode', action='store_true')
    parser.add_argument('-r', '--rate', dest='rate', help='set scale value [default=1.0]', default=1.0, type=float)
    parser.add_argument('-s', '--store', dest='store', help='folder to store file collection [default="store"]', default='store')
    return parser.parse_args()


def main():
    args = argument_parser()

    dataset = glob.glob(os.path.join(args.image_folder, "*"))
    # os.makedirs(args.store, exist_ok=True)

    index = 0
    while index < len(dataset):
        image = cv2.imread(dataset[index])
        image_name = os.path.basename(dataset[index])
        # image_path = os.path.join(args.store, image_name)  
        num_img = int(image_name.split(".")[0][-4:])
        label_name = "gt_"+str(num_img)+".txt"
        label_path = os.path.join(args.labels_path, label_name)
        rois, texts = take_rois_texts(label_path)
        index = debugger(image_name, image, rois,texts, args.watch, args.rate, index)



if __name__ == '__main__':
    main()
