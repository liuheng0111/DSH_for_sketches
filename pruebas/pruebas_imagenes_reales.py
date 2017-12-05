from pruebas_entre_sketches import computeMap, computePresition
import sys
sys.path.insert(0, '..')
import code
from scipy.spatial import distance
import os

def computeQuery(query_fname, query_clase,vectors,net):
    vecinos_mas_cercanos = [None]*50
    vecinos_mas_cercanos_d = [99999999]*50
    query_vector = code.getVector(query_fname,net)

    for (clase,vector) in vectors:
        dist = distance.euclidean(vector,query_vector)
        for i in range(50):
            if dist<vecinos_mas_cercanos_d[i]:
                vecinos_mas_cercanos_d[i]=dist
                vecinos_mas_cercanos[i]=clase
                break
    MaP = computeMap(query_clase,vecinos_mas_cercanos)
    presicion = computePresition(query_clase,vecinos_mas_cercanos)
    return (MaP,presicion)

def main():
    net = code.getNet(code.NORMAL_FINETUNE)
    #leer categorias
    categorias = []
    for linea in open('categoriesf.txt'):
        categorias.append(linea.strip())

    #leer vectores
    vectores = []
    for linea in open('vectores.csv'):
        l = linea.strip().split(';')
        clase = l[0]
        vector = map(float,l[2:-1])
        vectores.append((clase,vector))

    #test
    output = open('im_reales.csv','w')
    output.write('Categoria\tMaP\tPrecision\n')
    n = 0
    map_sum = 0
    prec_sum = 0
    for cat in categorias:
        n+=1
        print('Computando para categoria '+cat)
        n_c = 0
        map_sum_c=0
        prec_sum_c=0
        for fname in os.listdir('dataset_f/query/'+cat):
            if fname.endswith('.png'):
                path = 'dataset_f/query/'+cat+'/'+fname
                (MaP,prec) = computeQuery(path, cat,vectores,net)
                map_sum_c+=MaP
                prec_sum_c+=prec
                n_c+=1
                
        print("MaP: "+str(map_sum_c/n_c)+"; Prec: "+str(prec_sum_c/n_c))
        output.write(cat+"\t"+str(map_sum_c/n_c)+"\t"+str(prec_sum_c/n_c)+'\n')
        map_sum+=(map_sum_c/n_c)
        prec_sum+=(prec_sum_c/n_c)
    output.close()
    print('MaP general: '+str(map_sum/n)+"; Prec general: "+str(prec_sum/n))


if __name__=="__main__":
    main()