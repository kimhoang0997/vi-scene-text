#!/usr/bin/env python
import argparse, json, shutil
from PIL import Image, ImageFont
from uuid import uuid4
from random import shuffle, randint, random
from glob import glob
from os import path, makedirs
from test_random_aug import Random_StrAug


def preprocess():
    parser = argparse.ArgumentParser(description='Create trainning word-image dataset by dictionaries')
    parser.add_argument('-o', '--output', metavar="output-folder", default="output", help='folder that stores output files [default=output]')
    parser.add_argument('-c', '--config', metavar="config-file", default="data-augmentation-tool.json", help='data augmentation config file')
    parser.add_argument('-t', '--image-type', default=".jpg", choices=[".jpg", ".png", ".bmp"], help='image type of image dataset [default=.jpg]')
    parser.add_argument('-n', '--number-words', type=int, default=50000, help='number of words in trainning dataset [default=50000]')
    parser.add_argument('-r', '--remove-existed-output', action='store_true', help='remove existed files in output folders')
    parser.add_argument('-a', '--augmentation', action='store_true', help='apply data augmentation to the output images')
    args = parser.parse_args()

    if args.number_words < 30:
        parser.error("Minimum number of words  is 30")
    if args.remove_existed_output and path.exists(args.output):
        shutil.rmtree(args.output)


    makedirs(args.output, exist_ok=True)
    return args


def load_config(config_file):
    with open(config_file, encoding='utf-8') as file:
        config = json.load(file)
    total_rate = sum([dictionary["ratio"] for dictionary in config["dictionaries"]])
    for dictionary in config["dictionaries"]:
        dictionary["ratio"] = dictionary["ratio"] / total_rate
    return config

def get_font_paths(fonts_folder):
    return glob(path.join(fonts_folder, "*"))  


def create_word_bank(dictionaries, number_words):
    word_bank = []
    for dictionary in dictionaries:
        number_words_in_dictionary = round(number_words * dictionary["ratio"])
        with open(dictionary["path"], encoding='utf-8') as dictionary_file:
            dictionary_words = dictionary_file.readlines()
            shuffle(dictionary_words)
        
        for words_index in range(number_words_in_dictionary):
            number_word_of_dictionary = len(dictionary_words)
            dictionary_index = words_index % number_word_of_dictionary
            word = dictionary_words[dictionary_index].strip()
            word_bank.append(word)

    return word_bank

def random_ratio_padding(padding_ratio):
    ratio_padding = padding_ratio["min"] + (padding_ratio["max"] - padding_ratio["min"]) * random()
    return ratio_padding


def create_word_image(font, word, padding_ratio):
    background_color = (randint(0, 255), randint(0, 255), randint(0, 255))
    word_color = (randint(0, 255), randint(0, 255), randint(0, 255), randint(25, 255))

    word_mask = font.getmask(word, "L")
    word_mask_image = Image.new("RGBA", word_mask.size, color=background_color)
    word_mask_image.im.paste(word_color, (0, 0) + word_mask.size, word_mask)

    word_mask_width = word_mask.size[0]
    word_mask_height = word_mask.size[1]

    top_padding = int(word_mask_height * random_ratio_padding(padding_ratio))
    bottom_padding = int(word_mask_height * random_ratio_padding(padding_ratio))
    left_padding = int(word_mask_width * random_ratio_padding(padding_ratio))
    right_padding = int(word_mask_width * random_ratio_padding(padding_ratio))

    image_width = int(word_mask_width+left_padding+right_padding)
    image_height = int(word_mask_height+top_padding+bottom_padding)
    image_size = (image_width, image_height)
    # image_size = ((image_width if image_width < 65500 else 65500), (image_height if image_height < 65500 else 65500))

    start_point =  (left_padding, top_padding)

    image_object = Image.new("RGB", image_size, color=background_color)
    image_object.paste(word_mask_image, start_point)
    return image_object


def create_font(font_size_constraints, font_path):
    font_size = randint(font_size_constraints["min"], font_size_constraints["max"])
    font = ImageFont.truetype(font_path, size=font_size)
    return font


def save_word_bank_to_output_folder(
        word_bank, 
        font_paths, 
        output_folder,
        image_type, 
        label_file_name, 
        font_size_constraints,
        padding_ratio,
        augmentation):
    
    number_of_fonts = len(font_paths)
    label_file_path = path.join(output_folder, label_file_name)

    labels = []
    for word_index, word in  enumerate(word_bank):
        font_path = font_paths[word_index % number_of_fonts]
        font = create_font(font_size_constraints, font_path)
        
        image = create_word_image(font, word, padding_ratio)
        if augmentation:
            random_StrAug = Random_StrAug(using_aug_types = ['warp', 'geometry', 'blur', 'noise', 'camera', 'pattern', 'process', 'weather'],
                                  prob_list = [0.5, 0.3, 0.3, 0.2, 0.2, 0.1, 0.1, 0.1])
            image = random_StrAug(image)
        image_file_name = f"{uuid4()}{image_type}"
        word_image_file_path = path.join(output_folder, image_file_name)

        image.save(word_image_file_path)
        label = f"{word_index}\t{word}\t{image_file_name}\n"
        labels.append(label)

    with open(label_file_path, "a", encoding='utf-8') as label_file:
        label_file.writelines(labels)


def main():
    args = preprocess()
    config = load_config(args.config)
    font_paths = get_font_paths(config["fonts_folder"])
    word_bank = create_word_bank(config["dictionaries"], args.number_words)
    save_word_bank_to_output_folder(
        word_bank, 
        font_paths, 
        args.output, 
        args.image_type,
        config["label_file_name"],
        config["font_size_constraints"],
        config["padding_ratio"],
        args.augmentation
    )

if __name__ == '__main__':
    main()






