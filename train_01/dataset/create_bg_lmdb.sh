python ../../../caffe/scripts/create_annoset.py \
    --anno-type=detection\
    --label-type=txt \
    --label-map-file=labelmap_car_logo.prototxt \
    --min-dim=0 --max-dim=0 \
    --resize-width=0 \
    --resize-height=0 \
    --encode-type=jpg \
    --encoded \
    /home/figo/work/gitwork/caffe/train_01/data \
    /home/figo/work/gitwork/caffe/train_01/data/bg_image_list.txt \
    /home/figo/work/gitwork/caffe/train_01/dataset/bg_images_lmdb \
    .


