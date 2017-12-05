import sys
import os
from scipy.spatial import distance
import datetime
sys.path.insert(0, '..')
import code
def appendToFile(filename,data):
	f = open(filename,'a')
	f.write(data)
	f.close()

def writeLog(line):
	lf = open('log_file.txt','a')
	lf.write('{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())+" "+line+'\n')
	lf.close()
def computeMap(query_cat,vecinos):
	n = 0
	s = 0
	for i in range(len(vecinos)):
		pos = i+1
		if vecinos[i]==query_cat:
			n+=1
			s+=(1.0*n/pos)
	if n==0: 
		return 0
	return s/n
def computePresition(query_cat,vecinos):
	n = 0
	s = 0
	for i in range(len(vecinos)):
		n+=1
		if vecinos[i]==query_cat:
			s+=1
	return s*1.0/n

def computeMapTest(net,ds,cats):
	query_folder = ds+"/query"
	test_folder = ds+"/test"
	n = 0
	se_map = 0
	sh_map = 0
	se_prec = 0
	sh_prec = 0
	test_cache = {}
	fst = True
	for query_cat in cats:
		n_c = 0
		sce_map = 0
		sch_map = 0
		sce_prec = 0
		sch_prec = 0
		print('{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())+" Consultas para categoria "+query_cat)
		query_list = os.listdir(query_folder+"/"+query_cat)
		query_list.sort()
		for query_im in query_list:
			if query_im.endswith('.png'):
				vecinos_m_c_e = [None]*50
				vecinos_m_c_d_e = [9999999]*50
				vecinos_m_c_h = [None]*50
				vecinos_m_c_d_h = [9999999]*50
				query_vector = code.getVector(query_folder+"/"+query_cat+"/"+query_im,net)
				query_bin = code.getCode(query_vector)
				for test_cat in cats:
					if fst:
						print('{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())+" "+query_cat+"/"+query_im+" con "+test_cat)
					test_list = os.listdir(test_folder+"/"+test_cat)
					for test_im in test_list:
						if test_im.endswith('.png'):
							file_key = test_cat+"/"+test_im
							if file_key in test_cache:
								test_vector = test_cache[file_key]
							else:
								test_vector = code.getVector(test_folder+"/"+test_cat+"/"+test_im,net)
								test_cache[file_key] = test_vector
							test_bin = code.getCode(test_vector)
							euclidean = distance.euclidean(query_vector,test_vector)
							hamming = distance.hamming(query_bin,test_bin)
							for i in range(50):
								if euclidean<vecinos_m_c_d_e[i]:
									vecinos_m_c_d_e[i]=euclidean
									vecinos_m_c_e[i] = test_cat
									break
							for i in range(50):
								if hamming<vecinos_m_c_d_h[i]:
									vecinos_m_c_d_h[i] = hamming
									vecinos_m_c_h[i] = test_cat
									break
				e_map = computeMap(query_cat,vecinos_m_c_e)
				h_map = computeMap(query_cat,vecinos_m_c_h)
				e_prec = computePresition(query_cat,vecinos_m_c_e)
				h_prec = computePresition(query_cat,vecinos_m_c_h)
				if fst:
					print(vecinos_m_c_e[:10])
					print(vecinos_m_c_h[:10])
					print("MaP euclidean: "+str(e_map)+" - MaP hamming: "+str(h_map))
					print("Prec euclidean: "+str(e_prec)+" - Prec hamming: "+str(h_prec))
				n_c+=1
				sce_map +=e_map
				sch_map +=h_map
				sce_prec +=e_prec
				sch_prec +=h_prec

		n+=1
		se_map+= (sce_map/n_c)
		sh_map+= (sch_map/n_c)
		se_prec+=(sce_prec/n_c)
		sh_prec+=(sch_prec/n_c)
		print("MaP para clase "+query_cat+": Euclidean:"+str(sce_map/n_c)+", Hamming:"+str(sch_map/n_c))
		print("Prec para clase "+query_cat+": Euclidean:"+str(sce_prec/n_c)+", Hamming:"+str(sch_prec/n_c))
		writeLog("MaP para clase "+query_cat+": Euclidean:"+str(sce_map/n_c)+", Hamming:"+str(sch_map/n_c))
		writeLog("MaP para clase "+query_cat+": Euclidean:"+str(sce_map/n_c)+", Hamming:"+str(sch_map/n_c))
		fst = False	
	return(se_map/n,sh_map/n,se_prec/n,sh_prec/n)
def main():

	datasets = [('dataset_1','categories1.txt'),('dataset_2','categories2.txt'),('dataset_3','categories3.txt')]
	datasets_c = []
	for (ds,cat_f) in datasets:
		cats = []
		for linea in open(cat_f):
			cats.append(linea.strip())
		datasets_c.append((ds,cats))

	nets = [(code.getNet(code.MODIFY),'Modificado'),\
	(code.getNet(code.MODIFY_FINETUNE),'Modificado con Finetune'), \
	(code.getNet(code.MODIFY_SMALL),'Modificado Small'),\
	(code.getNet(code.MODIFY_SMALL_FINETUNE),'Modificado Small con Finetune'), \
	(code.getNet(code.NORMAL),'Normal'),\
	(code.getNet(code.NORMAL_FINETUNE),'Normal con Finetune'), \
	(code.getNet(code.NORMAL_SMALL),'Normal Small'),\
	(code.getNet(code.NORMAL_SMALL_FINETUNE),'Normal Small con Finetune')]

	resultados_me = 'MaP_euclidean.csv'
	resultados_mh = 'MaP_hamming.csv'
	resultados_pe = 'prec_euclidean.csv'
	resultados_ph = 'prec_hamming.csv'

	appendToFile(resultados_me,"Net/dataset\tdataset_1\tdataset_2\tdataset_3\n")
	appendToFile(resultados_mh,"Net/dataset\tdataset_1\tdataset_2\tdataset_3\n")
	appendToFile(resultados_pe,"Net/dataset\tdataset_1\tdataset_2\tdataset_3\n")
	appendToFile(resultados_ph,"Net/dataset\tdataset_1\tdataset_2\tdataset_3\n")


	for (net,net_name) in nets:
		appendToFile(resultados_me,net_name+'\t')
		appendToFile(resultados_mh,net_name+'\t')
		appendToFile(resultados_pe,net_name+'\t')
		appendToFile(resultados_ph,net_name+'\t')
		for (ds,cats) in datasets_c:
			print("Calculando MaP de "+net_name+" con "+ds)
			writeLog("** Net: "+net_name+" - Dataset: "+ds)
			(resp_me,resp_mh,resp_pe,resp_ph) = computeMapTest(net,ds,cats)
			print("MaP con vector: "+str(resp_me))
			print("MaP con cod. binario: "+str(resp_mh))
			print("Prec con vector: "+str(resp_pe))
			print("Prec con cod. binario: "+str(resp_ph))
			appendToFile(resultados_me,str(resp_me)+'\t')
			appendToFile(resultados_mh,str(resp_mh)+'\t')
			appendToFile(resultados_pe,str(resp_pe)+'\t')
			appendToFile(resultados_ph,str(resp_ph)+'\t')
		appendToFile(resultados_me,'\n')
		appendToFile(resultados_mh,'\n')
		appendToFile(resultados_pe,'\n')
		appendToFile(resultados_ph,'\n')
if __name__=="__main__":
    main()