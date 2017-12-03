#!/usr/bin/env sh

#TOOLS=/home/rromero/gsdk/bin
TOOLS=/path/to/gsdk/bin

$TOOLS/gsutil cp -r gs://quickdraw_dataset/full/binary/ \
  proyecto_sketches/quickdraw_binary/
