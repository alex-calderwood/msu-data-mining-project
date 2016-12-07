import numpy as np

from munkres import Munkres

def nb_words_calc(docs) : 
	nb_words_tot = 0
	for i in range(0,len(docs)) : 
		for key in docs[i] : 
			nb_words_tot += (docs[i])[key]
	return nb_words_tot

def transpose_doc(docs, nb_words) : 
	docs_mat = list()
	for i in range(0,nb_words):
		ligne = list()
		for j in range(0,len(docs)):
			if str(i+1) in docs[j]:
				ligne.append((docs[j])[str(i+1)])
			else : 
				ligne.append(0)
		docs_mat.append(ligne)
	return docs_mat 

def perplexity(docs, docs_transp, phi, theta):
    return np.exp(-sum(sum(docs_transp * np.dot(phi, theta))) / np.shape(docs)[0])
	
class PLSA(object):
    def __init__(self, num_topics, num_words, num_docs):
        self._num_topics = num_topics
        # Initialize theta and phi matrices
        self._num_docs = num_docs
        self._num_words = num_words
        self._theta_mat = np.random.uniform(0, 1, (num_topics, num_docs))
        self._theta_mat = self._theta_mat / sum(self._theta_mat)
        self._phi_mat = np.random.uniform(0, 1, (num_words, num_topics))
        self._phi_mat = self._phi_mat / sum(self._phi_mat)
    
    @property
    def phi(self): return self._phi_mat
    
    @property
    def theta(self): return self._theta_mat

    def estimate_phi_theta(self, docs, converge_par=1e-15, max_itr=100):
        docs_transp = transpose_doc(docs, self._num_words)
        perp_list = [(np.exp(- sum(sum(docs_transp * np.dot(self._phi_mat, self._theta_mat))) / self._num_docs))]
        doc_lengths = nb_words_calc(docs)
        for itr in range(0, max_itr):
            print ('EM iteration ' + str(itr + 1))
            # Initialization
            phi_mat = self._phi_mat
            theta_mat = self._theta_mat
            word_doc_mat = np.dot(phi_mat, theta_mat)
            #initialisation of the two matrices \Theta and \Phi
            word_topic_mat = np.zeros((self._num_words, self._num_topics))
            doc_topic_mat = np.zeros((self._num_docs, self._num_topics))
            topic_vec = np.zeros((self._num_topics, 1))
            for doc_idx in range(0, self._num_docs):
                if ((doc_idx + 1) % 50) == 0 :
                    print( str(doc_idx + 1) + ' documents processed, ' + str(int(50. * (doc_idx + 1) / self._num_docs)) + '% of the total amount')
                for word in docs[doc_idx]:#loop on words
                    for topic_idx in range(0, self._num_topics):#loop on topic
                        summand = (docs[doc_idx])[word] * phi_mat[(int(word))-1][topic_idx] * \
                            theta_mat[topic_idx][doc_idx] / word_doc_mat[(int(word))-1][doc_idx]
                        word_topic_mat[(int(word))-1][topic_idx] += summand
                        doc_topic_mat[doc_idx][topic_idx] += summand
                        topic_vec[topic_idx] += summand
            self._phi_mat = np.divide(word_topic_mat, np.transpose(np.tile(topic_vec, (1, self._num_words))))
            self._theta_mat = np.transpose(doc_topic_mat / np.transpose(np.tile(doc_lengths, (self._num_topics, 1))))
            
            perp = perplexity(docs, docs_transp, self._phi_mat, self._theta_mat)
            print ('Perplexity ' + str(perp))
            perp_list.append(perp)
            
            # Check convergence
            phi_diff = np.max(np.abs(phi_mat - self._phi_mat))
            theta_diff = np.max(np.abs(theta_mat - self._theta_mat))
            print ('Phi diff: ' + str(phi_diff) + '; Theta diff: ' + str(theta_diff))
            if max(phi_diff, theta_diff) < converge_par:
                print ('Algorithm converged.')
                break   
        return perp_list
        
    def return_docs_topics(self, docs):
        #tops = np.dot(docs, self._phi_mat)
        #return np.argmax(tops, 1)
        return np.argmax(self._theta_mat, 0)      