#!/usr/bin/python
import sys, os
import string, re
import numpy as np
import math 
import matplotlib.pylab as plt
from sortedcontainers import SortedDict
from collections import defaultdict

from plsa_sparse import PLSA

# Vocabulary filepath
voc_fname = os.path.join('voc.txt')
# Documents filepath
#docs_fpath = os.path.join('Filter')
docs_fname =  'representation_tf.txt'
#mat file_path (saving initial and final matrix parameters phi and theta)
init_phi_mat = os.path.join('init_phi_mat.txt')
init_theta_mat = os.path.join('init_theta_mat.txt')
end_phi_mat = os.path.join('phi_mat.txt')
end_theta_mat = os.path.join('theta_mat.txt')

def parse_docs_file(docs_fullfname):
    docs = list()
	
    with open(docs_fullfname, 'r') as docs_file:
        for line in docs_file:
            line = line.replace('\n', '')
			#print 'Document number ' + str(nb_doc)
            docs.append(map(int, line.split(',')))
			#nb_doc += 1
    return docs

def parse_docs_sparse(docs_fullfname):
	docs = list()
	
	with open(docs_fullfname, 'r') as docs_file:
		for line in docs_file:
			line = line.replace('\n', '')
			doc = SortedDict(defaultdict(int))
			word_list = line.split(' ')
			for i in range(0,len(word_list)):
				word = word_list[i].split(':')
				if len(word)==2 : 
					doc[word[0]] = int(word[1])
			docs.append(doc)
		return docs
	
#Parse the vocabulary into a list 
def parse_voc_file(voc_fullfname):
    voc = list()
    with open(voc_fullfname, 'r') as voc_file:
        for line in voc_file:
            line = line.replace('\n', '')
            voc.append(line.split()[1])
    return voc

def get_clustering_matrix(cluster_vec):
    cluster_mat = np.zeros((len(cluster_vec), len(cluster_vec)))
    for obj_idx in xrange(0, len(cluster_vec)):
        cluster_mat[obj_idx] = np.array([obj == cluster_vec[obj_idx] for obj in cluster_vec])
    return cluster_mat
	
def plot_clustering(clustering_vec):
    clustering_mat = get_clustering_matrix(clustering_vec)
    plt.figure()
    plt.imshow(clustering_mat, interpolation='nearest', cmap=plt.cm.ocean)
    return

def divergence_KL(init_mat, end_mat, n,m):
	summand = 0
	
	for i in range(0,n):
		for j in range(0,m):
			summand += (end_mat[i][j] * math.log(end_mat[i][j]/init_mat[i][j]))
	return summand
	
def write_mat(mat,n,m,name_file):
	filetxt = open(name_file,'w')
	for i in range(0,n):
		for j in range(0,m):
			filetxt.write( str(mat[i][j])+' ')
		filetxt.write('\n')
			
def _main():
    #NUM_DOCS = 100 # fixit
    EM_CONVERGENCE = 5e-5
    EM_MAX_ITR = 1000
    EM_MAX_ITR_THETA = 25
	
    # Parse docs file
    print ('Parsing docs file ' + docs_fname + '...')
    docs = parse_docs_sparse(docs_fname)

    print ('Parsing complete, total number of documents is ' + str(len(docs)) + '.')
	
	# Parse voc file
    voc = parse_voc_file(voc_fname)
	
    REG_VALUES = [0]
    # PLSA
    for reg_value in REG_VALUES:
        print ('Current reg value: ' + str(reg_value))
        plsa = PLSA(20, len(voc), len(docs))
		#Save init matrix
        init_phi = plsa.phi
        init_theta = plsa.theta
        write_mat(init_phi,len(voc),20,init_phi_mat)
        write_mat(init_theta,20,len(docs),init_theta_mat)
        print ('Start estimation.')
        print ('===================================')
        perplexity = plsa.estimate_phi_theta(docs, EM_CONVERGENCE, EM_MAX_ITR)
		#Save matrix at the end
        end_phi = plsa.phi
        end_theta = plsa.theta
        write_mat(end_phi,len(voc),20,end_phi_mat)
        write_mat(end_theta,20,len(docs),end_theta_mat)
        plt.plot(perplexity)
        plot_clustering(np.argmax(plsa.theta, axis=0))
        plot_clustering(plsa.return_docs_topics(docs))     
    
    plt.show()

if  __name__ == '__main__':
    _main()