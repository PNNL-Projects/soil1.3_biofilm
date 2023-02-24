#!/usr/bin/env python3

import os, sys
from skimage import io 
import glob
import numpy as np 

def simple_stitch(imgs, seq_num = 4, hr_margin = 233, vu_margin = 0):
    images = []
    for i in range(seq_num):
        img = imgs[i]
        if i < 3:
            images.append(img[:,:-hr_margin])
        else:
            images.append(img)
    img1 = np.hstack(images)
    images = []
    for i in range(seq_num):
        img = imgs[i+seq_num]
        if i < 3:
            images.append(img[:,:-hr_margin])
        else:
            images.append(img)
    img2 = np.hstack(images)
    im_h = np.vstack([img1[vu_margin:, :], img2[vu_margin:, :]])
    return(im_h)
def simple_stitch_z(imgs, z_num = None, seq_num = 4, hr_margin = 233, vu_margin = 0):
    if z_num == None:
        z_num = len(imgs[0])
    stitched = []
    for i in range(z_num):
        images = [img[i] for img in imgs]
        stitched.append(simple_stitch(images, seq_num, hr_margin, vu_margin))
    return(np.array(stitched))

img_root_dir = sys.argv[1]
img_dirs = [name for name in os.listdir(img_root_dir) if os.path.isdir(os.path.join(img_root_dir, name))] 

# Stitch all the BF figures and keep z stacks
for chi, channel in enumerate(['w1SD BF']):
# for chi, channel in enumerate(['w1SD BF', 'w2SD DAPI', 'w3SD GFP', 'w4SD RFP']):
    for dir in img_dirs:
        img_dir = img_root_dir + '/' + dir 
        print("Processing " + img_dir)
        tif_files = glob.glob(img_dir + '/' + dir + '_1_{}_s*.TIF'.format(channel))
        tif_files.sort()
        tif_file_new = img_dir + '/' + dir + '_1_{}_stitched.TIF'.format(channel)
        imgs = [io.imread(tif_file) for tif_file in tif_files]
        if chi == 0:
            imgzn = simple_stitch(imgs)
        else:
            imgzn = simple_stitch_z(imgs)
        io.imsave(tif_file_new, imgzn)
