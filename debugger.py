#!/usr/bin/env python

import sys
sys.path.append('/Users/hoangnguyen/GitHub/vi-scene-text')

import argparse, cv2, glob, os, math
import numpy as np
from paddleocr import PaddleOCR
from tools.infer.predict_det import TextDetector 
from tools.infer.predict_rec import TextRecognizer
from tools.infer.utility import get_rotate_crop_image,draw_ocr_box_txt
from PIL import Image, ImageDraw, ImageFont


def create_label(filename, tag):
    print(f"Created label for {filename}")

def remove_label(filename):
    print(f"Created label of {filename}")

def b_boxes(box):
    x0 = box[0][0]
    y0 = box[0][1]
    x1 = box[1][0]
    y1 = box[1][1]
    x2 = box[2][0]
    y2 = box[2][1]
    x3 = box[3][0]
    y3 = box[3][1]
    angle03 = math.atan2(y0 - y3, x0 - x3)
    angle12 = math.atan2(y1 - y2, x1 - x2)
    if (y0 - y3)/(x0 - x3) < 2:
        anpha = 30
    elif (y0 - y3)/(x0 - x3) < 4:
        anpha = 15
    else:
        anpha = 5
    increase03 = (y3-y0)*anpha/100
    increase12 = (y2-y1)*anpha/100
    x03 = increase03*math.cos(angle03)
    y03 = increase03*math.sin(angle03)
    x12 = increase12*math.cos(angle12)
    y12 = increase12*math.sin(angle12)
    x0 = x0 + x03
    y0 = y0 + y03
    x3 = x3 - x03
    y3 = y3 - y03
    x1 = x1 + x12
    y1 = y1 + y12
    x2 = x2 - x12
    y2 = y2 - y12
    box=[[x0,y0],[x1,y1],[x2,y2],[x3,y3]]
    return box 

def cv2_img_add_text(img, text, left_corner: (int, int),
                     text_rgb_color=(255, 255, 255), text_size=12, font='dataset/fonts/arial.ttf', **option):
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


# Debugger for tag from ocr.ocr
def debugger(filename, image, rois,texts,scores, watch, rate, index):
    font = cv2.FONT_HERSHEY_SIMPLEX
    green = (80, 220, 60)
    yellow = (255, 0, 0)
    img = cv2.resize(image, None, fx=rate, fy=rate)
    font_size = img.shape[1]//50
    drop_score = 0.5
    font_path = "dataset/fonts/arial.ttf"

    # for i in range(len(rois)):
    #     roi = rois[i]
    #     text = texts[i]
    #     cv2.polylines(img, [(rate*np.array(roi)).astype(np.int64)], True, green, 2)
    #     img = cv2_img_add_text(img, str(i+1), (int(rate*roi[0][0]), int(rate*roi[0][1])-font_size), text_rgb_color=yellow, text_size=font_size, font='./arial.ttf')
    # if texts is not None:
    #     img_add = np.array(resize_img(img, input_size=600))
    #     txt_img = text_visual(
    #         texts,
    #         scores,
    #         img_h=img_add.shape[0],
    #         img_w=600,
    #         threshold=drop_score,
    #         font_path=font_path)
    #     img = np.concatenate([np.array(img_add), np.array(txt_img)], axis=1)
    image = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    draw_img = draw_ocr_box_txt(
                    image,
                    np.array(rois),
                    texts,
                    scores,
                    drop_score=drop_score,
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
    parser = argparse.ArgumentParser(description='Detector with paddleoce knowledge for image datasets')
    parser.add_argument('image_folder', help='the image folder for processing')
    parser.add_argument('-w', '--watch', dest='watch', help='set watch mode', action='store_true')
    parser.add_argument('-r', '--rate', dest='rate', help='set scale value [default=1.0]', default=1.0, type=float)
    parser.add_argument('-s', '--store', dest='store', help='folder to store file collection [default="store"]', default='store')
    return parser.parse_args()

class TextDetectorParamters():
    def __init__(self): 
        self.det_algorithm = "DB"
        self.use_onnx = False
        self.det_limit_side_len = 960       
        self.det_limit_type = 'max'         
        self.det_db_thresh=0.3
        self.det_db_box_thresh = 0.6
        self.det_db_unclip_ratio= 1.5
        self.use_dilation=False
        self.det_db_score_mode= "fast"
        self.max_batch_size= 10
        self.det_box_type="quad"
        self.det_model_dir="inference/det/en_PP-OCRv3_det_infer"
        self.use_gpu = False
        self.benchmark= "F-score"
        self.use_npu=False
        self.use_xpu=False
        self.enable_mkldnn=False
        self.precision="fp32"


class TextRecognizerParamters():
    rec_algorithm = "SVTR_LCNet"
    rec_batch_num = 256
    rec_char_dict_path = 'ppocr/utils/dict/vi_dict.txt'
    rec_model_dir = "inference/rec/v3_vi_mobile_aug"
    use_space_char = True
    benchmark = False
    use_onnx = False
    use_gpu = False
    enable_mkldnn = False
    use_npu = False
    use_xpu = False
    warmup = False
    rec_image_shape = "3, 48, 320"

def text_recognizer(image,rois):
    paramters_rec = TextRecognizerParamters()
    recognizer = TextRecognizer(paramters_rec)
    list = []
    for roi in rois:
        roi = get_rotate_crop_image(image, np.float32(roi))
        list.append(roi)    
    txts, _ = recognizer(list)
    texts = [txt[0] for txt in txts]
    scores = [txt[1] for txt in txts]
    return texts, scores

def main():
    args = argument_parser()
    # ocr = PaddleOCR(use_angle_cls=True, lang='en')

    paramters_det = TextDetectorParamters()
    detector = TextDetector(paramters_det)

    dataset = glob.glob(os.path.join(args.image_folder, "*"))
    os.makedirs(args.store, exist_ok=True)

    index = 0
    while index < len(dataset):
        image = cv2.imread(dataset[index])
        filename = os.path.join(args.store, os.path.basename(dataset[index]))  
        # tag = ocr.ocr(image, cls=True)[0]
        rois, elapse = detector(image)
        texts,scores = text_recognizer(image,rois)
        index = debugger(filename, image, rois,texts,scores, args.watch, args.rate, index)



if __name__ == '__main__':
    main()
