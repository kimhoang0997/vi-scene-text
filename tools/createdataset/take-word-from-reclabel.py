from os import path, makedirs
from uuid import uuid4
from PIL import Image
import argparse, cv2, json


def preprocess():
    parser = argparse.ArgumentParser(description='Detector with paddleocr knowledge for image datasets')
    parser.add_argument('-c','--config', default="configs/createdataset/take-word-from-dictguide-label.json", help='take word from dictguide config file')
    parser.add_argument('-it', '--inputimagetype',default= 'JPG', help='input image type file')
    parser.add_argument('-ot', '--outputimagetype', default= 'JPG', help='set watch mode')
    args = parser.parse_args()
    return args

def load_config(config_file):
    with open(config_file, encoding='utf-8') as file:
        config = json.load(file)
    return config

def crop_image(image_path,roi, OUTPUT_FOLDER, OUTPUT_IMAGE_TYPE):
    image = cv2.imread(image_path)
    image_crop = image[int(roi[1]):int(roi[3]),int(roi[0]):int(roi[2])]
    new_image_name = str(uuid4()) + "." + OUTPUT_IMAGE_TYPE
    new_image_path = path.join(OUTPUT_FOLDER,new_image_name)
    cv2.imwrite(new_image_path,image_crop)
    return new_image_name

def main():
    args = preprocess()
    config = load_config(args.config)

    makedirs(config["OUTPUT_FOLDER"], exist_ok=True)

    with open(config["LABEL_FILE"],"r", encoding="utf-8") as label_file:
        with open(config["OUTPUT_LABEL_FILE"],"w",encoding="utf-8") as output_label_file:
            labels = label_file.readlines()
            for line in labels[1:]:
                line = line.strip().split(",")
                image_path = line[0]
                label = line[3]
                roi = line[-4:]
                new_image_name = crop_image(image_path,roi,config["OUTPUT_FOLDER"], args.outputimagetype)
                output_label_file.write(new_image_name+"\t"+label+"\n")

if __name__ == '__main__':
    main()