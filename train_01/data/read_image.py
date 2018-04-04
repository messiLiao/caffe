# coding : utf-8
# encode : utf-8
import os
import re
import cv2
import caffe
import lmdb
import numpy as np
import random

def generate_labels_txt_file(images_dir, labels_dir, replace=False):
    
    if not os.path.isdir(labels_dir):
        os.mkdir(labels_dir)

    fn_list = os.listdir(images_dir)

    max_w = 60
    min_w = 20
    max_h = 60
    min_h = 20

    write = False
    for fn in fn_list:
        name, ext = os.path.splitext(fn)
        full_fn = os.path.join(images_dir, fn)
        image = cv2.imread(full_fn)

        sub_classes = random.randint(1, 4)
        label_lines = []
        h, w = image.shape[:2]
        for i in range(sub_classes):
            _w = random.randint(min_w, max_w)
            _h = random.randint(min_h, max_h)
            _x = random.randint(0, w - _w - 1)
            _y = random.randint(0, h - _h - 1)
            _label = random.randint(1, 20)
            label_line = "%d %d %d %d %d \n" % (_label, _x, _y, _x+_w, _y+_h)
            label_lines.append(label_line)

        label_fn = os.path.join(labels_dir, "%s.txt" % name)
        if (os.path.isfile(label_fn) and replace) or (not os.path.isfile(label_fn)):
            with open(label_fn, 'w') as fd:
                fd.writelines(label_lines)
            write = True

        print label_fn
    return write

def generate_anno_text_file(images_dir, labels_dir, anno_fn):
    image_fn_list = os.listdir(images_dir)
    anno_lines = []

    for image_fn in image_fn_list:
        _, img_fn = os.path.split(image_fn)
        name, ext = os.path.splitext(img_fn)
        label_fn = os.path.join(labels_dir, '%s.txt' % name)
        # print label_fn
        if not os.path.isfile(label_fn):
            print "label file %s is not exits" % label_fn
            continue
        # with open(label_fn, 'r') as fd:
        #     label_lines = fd.readlines()
        #     for label_line in label_lines:
        #         anno_line = '%s %s\n' % (img_fn, label_line.replace('\n', '').replace('\r', ''))
        #         anno_lines.append(anno_line)
        anno_lines.append("%s %s\n" % (os.path.join(images_dir, image_fn), label_fn))
    with open(anno_fn, 'w') as fd:
        print "lines :", len(anno_lines)
        fd.writelines(anno_lines)
    print "output file:", anno_fn
    pass
def read_db(db_path):
    lmdb_env = lmdb.open(db_path)
    lmdb_txn = lmdb_env.begin()
    lmdb_cursor = lmdb_txn.cursor()
    datum = caffe.proto.caffe_pb2.Datum() 

    for ( idx, (key, value) ) in enumerate(lmdb_cursor):

        datum.ParseFromString(value)
        if idx == 0:
            print dir(datum)
        label = datum.label
        print idx, key, label, datum.ByteSize(), datum.channels

        data = caffe.io.datum_to_array(datum)

        image = np.transpose(data, (1, 2, 0))
        cv2.imshow("lmdb_image", image)
        cv2.waitKey(0)

    lmdb_env.close()
    pass

def main(fn):
    train_images_list = []
    with open(fn, 'r') as fd:
        lines = fd.readlines()
        for line in lines:
            img_fn, class_id = line.split(' ')[:2]
            full_fn = os.path.join('images', img_fn)
            image = cv2.imread(full_fn, 1)
            print image.shape, int(class_id)
        pass
    pass

if __name__ == '__main__':
    train_fn = './images/train.txt'
    # main(train_fn)
    # read_db('../dataset/bg_images_lmdb')
    generate_labels_txt_file('./images', './labels', replace=True)
    generate_anno_text_file('./images', './labels', '../data/bg_image_list.txt')
