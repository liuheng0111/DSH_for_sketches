import caffe
import numpy as np
import sys
from PIL import Image

def getNet():
	model = 'deploy.prototxt'
	weights = 'quickdraw_iter_2000.caffemodel'
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
	probs = r['ip1'][0]
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
	if len(argv)<2:
		print "Uso: python code.py path_to_im"
		sys.exit(2)
	imfile = argv[1]
	net = getNet()
	vector = getVector(imfile,net)
	print vector
	code = getCode(vector)
	print code
	
if __name__ == "__main__":
	main(sys.argv)
