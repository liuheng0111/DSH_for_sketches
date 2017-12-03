
import struct
from struct import unpack
import numpy as np
from skimage.draw import line_aa
import scipy.misc
import os
import sys

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

#Script para generar base de dato para caffe
def main():
    if len(sys.argv)<=2:
        print("Uso: create_pictures.py input_quickdraw_dir output_quickdraw_dir offset(opcional)")
        return
    input_dir = sys.argv[1]
    output_dir = sys.argv[2]
    if not os.path.isdir(input_dir) or not os.path.isdir(output_dir):
        print("Error: Directorio no valido")
        return
    offset = 0
    if len(sys.argv)>3:
        offset = int(sys.argv[3])
    #obtener categorias
    #categories = []
    #for fname in os.listdir(input_dir):
    #    if os.path.isfile(input_dir+os.sep+fname):
    #        categories.append(fname)
    #categories.sort()
    #cargar categorias reales

    categories = []
    cat_file = open('categories.txt')    
    for linea in cat_file:
        linea = linea.strip().split(' ')
        categories.append(" ".join(linea[1:]))
    print("Numero de categorias totales: "+str(len(categories)))

    N=10000 #10000 imagenes por categoria
    itemid = 0
    train_file = open(output_dir+os.sep+"train.txt","w")
    for c in range(len(categories)):
        n=0
	print("Procesando: "+categories[c]+" "+str(c+1)+"/"+str(len(categories)))
        for drawing in unpack_drawings(input_dir+os.sep+categories[c]+".bin"):
            # do something with the drawing
	    n +=1
	    if n<offset:
		continue
	    if (n+1)% 500==0:
		print(str(n+1)+"/"+str(N+offset)+" datos")
            pic = np.zeros([256,256])+255
            for stroke in drawing['image']:
                x = stroke[0]
                y = stroke[1]
                for i in range(len(x)-1):
                    rr, cc, val = line_aa(y[i],x[i],y[i+1],x[i+1])
                    pic[rr, cc] = val
            save_image(pic,output_dir+"/"+str(itemid)+".png")
	    train_file.write(str(itemid)+".png "+str(c)+"\n")
            itemid +=1
            if n>=N+offset:
                break
    train_file.close()
if __name__=="__main__":
    main()
