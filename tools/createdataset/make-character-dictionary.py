#!/usr/bin/env python
import argparse
from glob import glob
from os import path


def preprocess():
    parser = argparse.ArgumentParser(description='Make character dataset from dictionaries.')
    parser.add_argument('folder', help='folder that stores dictionaries')
    parser.add_argument('output', help='character dataset file')
    return parser.parse_args()


def main():
    args = preprocess()
    characters = []
    dictionaries = glob(path.join(args.folder, "*"))
    for dictionary in dictionaries:
        with open(dictionary, encoding='utf-8') as dictionary:
            dictionary = dictionary.readlines()
            for line in dictionary:
                line = line.strip()
                for character in line:
                    if character not in characters:
                        characters.append(character)

    with open(args.output, "w", encoding='utf-8') as dictionary:
        for character in characters:
            dictionary.write(f"{character}\n")
            print(f"{character}")

if __name__ == '__main__':
    main()
