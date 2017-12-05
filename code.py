import caffe
import numpy as np
import sys
from PIL import Image

MODIFY=0
MODIFY_FINETUNE=1
MODIFY_SMALL=2
MODIFY_SMALL_FINETUNE=3
NORMAL=4
NORMAL_FINETUNE=5
NORMAL_SMALL=6
NORMAL_SMALL_FINETUNE=7
    
def getNet(tipo):
    model = 'deploy.prototxt'
    if tipo==MODIFY:
        weights = 'final_models/modify.caffemodel'
    elif tipo==MODIFY_FINETUNE:
        weights = 'final_models/modify_finetune.caffemodel'
        model = 'fine_deploy.prototxt'
    elif tipo==MODIFY_SMALL:
        weights = 'final_models/modify_small.caffemodel'
    elif tipo==MODIFY_SMALL_FINETUNE:
        weights = 'final_models/modify_small_finetune.caffemodel'
        model = 'fine_deploy.prototxt'
    elif tipo==NORMAL:
        weights = 'final_models/normal.caffemodel'
    elif tipo==NORMAL_FINETUNE:
        weights = 'final_models/normal_finetune.caffemodel'
        model = 'fine_deploy.prototxt'
    elif tipo==NORMAL_SMALL:
        weights = 'final_models/normal_small.caffemodel'
    else:
        weights = 'final_models/normal_small_finetune.caffemodel'
        model = 'fine_deploy.prototxt'
    caffe.set_mode_cpu()
    net = caffe.Net(model,weights,caffe.TEST)
    return net

def getVector(imname,net):
    im = np.array(Image.open(imname))
    im.reshape((256,256))
    im = im[np.newaxis,np.newaxis,:,:]
    net.blobs['data'].reshape(*im.shape)
    net.blobs['data'].data[...]=im
    r = net.forward()
    if 'ip1' in r:
        probs = r['ip1'][0]
    else:
        probs = r['ip1_f'][0]
    toret = []
    for p in probs:
        toret.append(p)
    return toret
def getVectorFromMat(immat,net):
    im = np.array(immat)
    im.reshape((256,256))
    im = im[np.newaxis,np.newaxis,:,:]
    net.blobs['data'].reshape(*im.shape)
    net.blobs['data'].data[...]=im
    r = net.forward()
    if 'ip1' in r:
        probs = r['ip1'][0]
    else:
        probs = r['ip1_f'][0]
    toret = []
    for p in probs:
        toret.append(p)
    return toret

def getCode(probs):
    bin = [0]*12
    for i in range(12):
            if probs[i]>0:
                bin[i]=1
    return bin

def main(argv):
    if len(argv)<3:
        print "Uso: python code.py path_to_im tipo\n\ttipo:\n\t\t0=modify\n\t\t1=modify finetune\n\t\t2=modify small\n\t\t3=modify small finetune"
        sys.exit(2)
    imfile = argv[1]
    net = getNet(int(argv[2]))
    vector = getVector(imfile,net)
    print vector
    code = getCode(vector)
    print code
    
if __name__ == "__main__":
    main(sys.argv)
