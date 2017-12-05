import cv2
import numpy as np
import scipy.ndimage
import sys
import os
sys.path.insert(0, '..')
import code

def getVector(file_name,net):
    img = cv2.imread(file_name,0)
    img = scipy.ndimage.median_filter(img,3)
    edges = cv2.Canny(img,100,200)
    final = np.invert(edges)
    final = cv2.resize(final,(256,256))
    vector = code.getVectorFromMat(final,net)
    return vector

def main():
    net = code.getNet(code.NORMAL_FINETUNE)
    #leer categorias
    categorias = []
    for linea in open('categoriesf.txt'):
        categorias.append(linea.strip())
    #archivo con vectores
    vectores = open('vectores.csv','w')
    for cat in categorias:
        print("Computando para "+cat)
        for fname in os.listdir('caltech/'+cat):
            if fname.endswith('.jpg'):
                path = 'caltech/'+cat+'/'+fname
                vector = getVector(path,net)
                vectores.write(cat+';'+path+';')
                for e in vector:
                    vectores.write(str(e)+';')
                vectores.write('\n')
    vectores.close()

if __name__=="__main__":
    main()