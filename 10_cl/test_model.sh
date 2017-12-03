#!/usr/bin/env sh

TOOLS=/home/rromero/deep-supervised-hashing-DSH/build/tools
export LD_LIBRARY_PATH=/home/rromero/deep-supervised-hashing-DSH/OpenBLAS/

$TOOLS/caffe test \
    --model=train_test.prototxt \
    --weights finetune_model/quickdraw_iter_8000.caffemodel --gpu=1
