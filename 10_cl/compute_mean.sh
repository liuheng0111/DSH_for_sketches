#!/usr/bin/env sh
#export LD_LIBRARY_PATH=/home/rromero/deep-supervised-hashing-DSH/OpenBLAS/
TOOLS=../deep-supervised-hashing-DSH/build/tools

$TOOLS/compute_image_mean quickdraw_lmdb_train quickdraw_train.binaryproto

$TOOLS/compute_image_mean quickdraw_lmdb_test quickdraw_test.binaryproto
