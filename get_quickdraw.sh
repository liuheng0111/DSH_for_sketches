#!/usr/bin/env sh

#TOOLS=/home/rromero/gsdk/bin
TOOLS=../google-cloud-sdk/bin
mkdir quickdraw_binary
$TOOLS/gsutil cp -r gs://quickdraw_dataset/full/binary/ \
  quickdraw_binary/
