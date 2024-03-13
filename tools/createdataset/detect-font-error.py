from os import path
from fontTools.ttLib import TTFont
from glob import glob
import unicodedata

FONTS_PATH = "fonts"
CHARACTERS_PATH = "characters.txt"


def char_in_font(unicode_char, font):
    for cmap in font['cmap'].tables:
        if cmap.isUnicode():
            if ord(unicode_char) in cmap.cmap:
                return True
    return False


fonts = glob(path.join(FONTS_PATH, "*"))

with open(CHARACTERS_PATH, encoding='utf-8') as file:
    lines = file.readlines()
    for font_path in fonts:
        for line in lines:
            char = line.strip()
            if char:
                font = TTFont(font_path)
                if not char_in_font(char, font):
                    print(char + " " + unicodedata.name(char) + " in " + font_path)
                    break


