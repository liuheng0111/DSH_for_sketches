#!/usr/bin/env sh

TOOLS=deep-supervised-hashing-DSH/build/tools
export LD_LIBRARY_PATH=deep-supervised-hashing-DSH/OpenBLAS/

$TOOLS/caffe test \
    --model=train_test.prototxt \
    --weights=final_models/modify.caffemodel --gpu=2
