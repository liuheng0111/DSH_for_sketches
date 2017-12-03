#!/usr/bin/env sh

export LD_LIBRARY_PATH=/home/rromero/deep-supervised-hashing-DSH/OpenBLAS/

TOOLS=/home/rromero/deep-supervised-hashing-DSH/build/tools

$TOOLS/caffe train \
    --solver=solver.prototxt #--gpu=1 #--snapshot=quickdraw_iter_4316.solverstate
