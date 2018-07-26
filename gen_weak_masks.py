import os, sys
import glob
import argparse
import datetime
import numpy as np
from tqdm import tqdm

from PIL import Image


annotation_version = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

ap = argparse.ArgumentParser()

ap.add_argument("-a", "--annotation_file",
                required=True,
                default=None,
                type=str,
                help="The annotation file in keras-yolo3 format. Eg, generated by darknet_annotation.py.")
ap.add_argument("-o", "--output_path",
                required=False,
                default='model_data/weak_masks/version_{}'.format(annotation_version),
                type=str,
                help="The dataset root path location.")

ARGS = ap.parse_args()

IMG_WIDTH = 640
IMG_HEIGHT = 480
with open(ARGS.annotation_file, 'r') as annot_f:
    for annot in tqdm(annot_f):
        # print(annot)
        # annot = 'img_path x_min,y_min,x_max,y_max,class_id x_min,y_min,x_max,y_max,class_id ...'
        destination_dir = os.path.join(ARGS.output_path, os.path.dirname(annot).replace('/home','home'))
        # print(destination_dir)
        os.makedirs(destination_dir, exist_ok=True)
        fg_mask = np.zeros((IMG_WIDTH, IMG_HEIGHT), dtype=np.uint8)
        annot = annot.split(' ')
        img_path = annot[0]
        bboxes = []
        for bbox in annot[1:]:
            x_min, y_min, x_max, y_max, class_id = list(map(int, bbox.split(',')))
            # fg_mask[y_min:y_max, x_min:x_max] = 1
            fg_mask[x_min:x_max, y_min:y_max] = 255

        Image.fromarray(fg_mask.T).save(os.path.join(destination_dir, 'fg.jpg'))
        Image.fromarray(np.invert(fg_mask.T)).save(os.path.join(destination_dir, 'bg.jpg'))

        # sys.exit()
