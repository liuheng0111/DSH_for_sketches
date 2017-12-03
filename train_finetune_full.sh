
#!/usr/bin/env sh

TOOLS=deep-supervised-hashing-DSH/build/tools

$TOOLS/caffe test \
    --model=train_test.prototxt \
    --weights fine_model/quickdraw_iter_7000.caffemodel




