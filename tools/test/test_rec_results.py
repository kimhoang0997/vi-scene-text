import sys
sys.path.append('/Users/hoangnguyen/GitHub/vi-scene-text')

from tools.infer.predict_rec import TextRecognizer
from glob import glob
from os import path, makedirs
import cv2
import shutil

images_path = "dataset/dictguide_label/vintext_3_2024/rec_test_image_63anh"
label_path = "dataset/dictguide_label/vintext_3_2024/rec_test_image_63anh/rec_gt_test_63anh.txt"
output_path = "dataset/dictguide_label/vintext_3_2024/rec_test_image_63anh/output"

class TextRecognizerParamters():
    rec_algorithm = "SVTR_LCNet"
    rec_batch_num = 256
    rec_char_dict_path = 'ppocr/utils/dict/vi_dict.txt'
    rec_model_dir = "inference/rec/vi_PP-OCRv3_rec"
    use_space_char = True
    benchmark = False
    use_onnx = False
    use_gpu = False
    enable_mkldnn = False
    use_npu = False
    use_xpu = False
    warmup = False
    rec_image_shape = "3, 48, 320"


cache = {}
with open(label_path, encoding="utf-8") as label_file:
    content = label_file.readlines()
    for line in content:
        name, label = line.replace("\n", "").split("\t")
        cache[name] = {
            "real_label": label
        }

paramters = TextRecognizerParamters()
text_recognizer = TextRecognizer(paramters)

for image_path in glob(path.join(images_path, "*.JPG")):
    img = cv2.imread(image_path)
    name = path.basename(image_path)
    cache[name]["img"] = img
    cache[name]["path"] = image_path

names = list(cache.keys())
list = [cache[name]["img"] for name in names]

rec_res, exec_time = text_recognizer(list)

for index, rec_re in enumerate(rec_res):
    name = names[index]
    cache[name]["rec_label"] = rec_re[0]
    cache[name]["prob"] = rec_re[1]
    cache[name]["is_correct"] = cache[name]["rec_label"] == cache[name]["real_label"]
        

if not path.exists(output_path):
    makedirs(output_path)

with open(path.join(output_path, "info.csv"), "w", encoding="utf-8") as file:
    headers = ",".join(["name", "real_label", "rec_label", "prob"])
    file.write(headers + "\n")
    n_pre = 0
    n = 0
    for name in names:
        if not cache[name]["is_correct"]:
            rows = ",".join([name, cache[name]["real_label"], cache[name]["rec_label"], str(cache[name]["prob"])])
            shutil.copyfile(cache[name]["path"], path.join(output_path, name))
            file.write(rows + "\n")
            n_pre +=1
        n += 1
    
acc = (n -n_pre)/n
print("Số ảnh: ",n, " Số dự đoán đúng: ", (n-n_pre),"acc: ", acc)

with open(path.join(output_path, "label.csv"), "w", encoding="utf-8") as file:
    for name in names:
        if not cache[name]["is_correct"]:
            rows = name + "\t" + cache[name]["real_label"]      
            file.write(rows + "\n")