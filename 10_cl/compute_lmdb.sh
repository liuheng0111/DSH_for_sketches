#!/usr/bin/env sh
#export LD_LIBRARY_PATH=deep-supervised-hashing-DSH/OpenBLAS/
TOOLS=../deep-supervised-hashing-DSH/build/tools

$TOOLS/convert_imageset --gray --shuffle \
  --resize_width=256 --resize_height=256 \
  quickdraw_trainset/ quickdraw_trainset/train.txt \
  quickdraw_lmdb_train 1 

$TOOLS/convert_imageset --gray --shuffle \
  --resize_width=256 --resize_height=256 \
  quickdraw_testset/ quickdraw_testset/train.txt \
  quickdraw_lmdb_test 1

