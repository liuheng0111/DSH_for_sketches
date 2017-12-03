#!/usr/bin/env sh

export LD_LIBRARY_PATH=/home/rromero/deep-supervised-hashing-DSH/OpenBLAS/
TOOLS=/home/rromero/deep-supervised-hashing-DSH/build/tools

$TOOLS/caffe train \
    --solver=finetune_solver.prototxt \
    --snapshot=quickdraw_iter_7000.solverstate --gpu 2
#    --weights=model_nm/quickdraw_iter_10000.caffemodel --gpu 2 #\
    #>>CIFAR-10/log.txt 2>&1 
