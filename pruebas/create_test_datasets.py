
import struct
from struct import unpack
import numpy as np
from skimage.draw import line_aa
import scipy.misc
import os

db = None
env = None

def unpack_drawing(file_handle):
    key_id, = unpack('Q', file_handle.read(8))
    countrycode, = unpack('2s', file_handle.read(2))
    recognized, = unpack('b', file_handle.read(1))
    timestamp, = unpack('I', file_handle.read(4))
    n_strokes, = unpack('H', file_handle.read(2))
    image = []
    for i in range(n_strokes):
        n_points, = unpack('H', file_handle.read(2))
        fmt = str(n_points) + 'B'
        x = unpack(fmt, file_handle.read(n_points))
        y = unpack(fmt, file_handle.read(n_points))
        image.append((x, y))

    return {
        'key_id': key_id,
        'countrycode': countrycode,
        'recognized': recognized,
        'timestamp': timestamp,
        'image': image
    }


def unpack_drawings(filename):
    with open(filename, 'rb') as f:
        while True:
            try:
                yield unpack_drawing(f)
            except struct.error:
                break        
    
def save_image(mat,file_name):
    scipy.misc.imsave(file_name, mat)

def main():
    crear_dir = True

    datasets = [('dataset_1','categories1.txt'),('dataset_2','categories2.txt'),('dataset_3','categories3.txt'),('dataset_f','categoriesf.txt')]
    binary_files_path = '../quickdraw_binary/binary'
    offset = 20000
    for (ds,cat_filename) in datasets:
        if crear_dir:
            os.mkdir(ds)
            os.mkdir(ds+'/query')
            os.mkdir(ds+'/test')
        categories = []
        for line in open(cat_filename):
            categories.append(line.strip())
        print("haciendo "+ds)
        for c in range(len(categories)):
            os.mkdir(ds+'/query/'+categories[c])
            os.mkdir(ds+'/test/'+categories[c])
            n=0
            r=0
            print("Procesando: "+categories[c]+" "+str(c+1)+"/"+str(len(categories)))
            for drawing in unpack_drawings(binary_files_path+os.sep+categories[c]+".bin"):
            # do something with the drawing
                if r<offset:
                    r+=1
                    continue
                n +=1
                pic = np.zeros([256,256])+255
                for stroke in drawing['image']:
                    x = stroke[0]
                    y = stroke[1]
                    for i in range(len(x)-1):
                        rr, cc, val = line_aa(y[i],x[i],y[i+1],x[i+1])
                        pic[rr, cc] = val
                if n>10:
                    save_image(pic,ds+"/test/"+categories[c]+"/"+str(n-10)+".png")
                else:
                    save_image(pic,ds+"/query/"+categories[c]+"/"+str(n)+".png")
                if n==110:
                    break

if __name__=="__main__":
    main()