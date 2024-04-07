import glob, os
from PIL import Image, ImageFont
from random import randint, random
from uuid import uuid4



def create_font(font_size_constraints, font_path):
    font_size = font_size_constraints
    font = ImageFont.truetype(font_path, size=font_size)
    return font

def create_word_image(font, word, padding_ratio):
    background_color = (255,255,255,255)
    word_color = (0,0,0,0)

    word_mask = font.getmask(word, "L")
    word_mask_image = Image.new("RGBA", word_mask.size, color=background_color)
    word_mask_image.im.paste(word_color, (0, 0) + word_mask.size, word_mask)

    word_mask_width = word_mask.size[0]
    word_mask_height = word_mask.size[1]

    top_padding = int(word_mask_height * 0.1)
    bottom_padding = int(word_mask_height * 0.1)
    left_padding = int(word_mask_width * 0.1)
    right_padding = int(word_mask_width * 0.1)

    image_width = int(word_mask_width+left_padding+right_padding)
    image_height = int(word_mask_height+top_padding+bottom_padding)
    image_size = (image_width, image_height)
    # image_size = ((image_width if image_width < 65500 else 65500), (image_height if image_height < 65500 else 65500))

    start_point =  (left_padding, top_padding)

    image_object = Image.new("RGB", image_size, color=background_color)
    image_object.paste(word_mask_image, start_point)
    return image_object



font_path = "dataset/3D-font"
word = "Chào bạn. Đây là font chữ 3D."

fonts = glob.glob(os.path.join(font_path,"*"))
for font_path in fonts:
    fontname = os.path.basename(font_path)
    font = create_font(40, font_path)
    image = create_word_image(font, word, padding_ratio=0.1)
    image.show(fontname)


