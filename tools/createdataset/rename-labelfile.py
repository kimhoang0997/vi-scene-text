import glob
import os

labels_path = "dataset/dictguide_rectlabel/labels"

labels = glob.glob(os.path.join(labels_path, "*"))

index = 0
while index < len(labels):
    label_path = os.path.dirname(labels[index])
    label_name = os.path.basename(labels[index])
    num = int(label_name.split(".")[0][3:])
    new_name = os.path.join(label_path,'im%04d.txt' % num)
    os.rename(labels[index], new_name)
    index += 1