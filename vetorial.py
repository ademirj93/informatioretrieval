import glob, nltk, re, heapq, numpy as np, math, statistics as sta, matplotlib.pyplot, csv
from pstats import Stats
from typing import Dict
from multiprocessing import Value
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from regex import W
nltk.download('stopwords')
nltk.download('punkt')

#conjunto de stop words em ingês
stopwordnltk = stopwords.words('english')
#variaveis de controle de Quantidade
tq = 0 
td = 0

#definição dos diretórios dentro das variaveis
querrydir = "./querry/**/*"
#querrydir = "./querry/alt.atheism/*"
datadir = "./dataset/**/*"
#datadir = "./Dataset_test/*.txt"

global_words_Token = []

count_glob = []

#identificando arquivos e diretórios em um array
all_datafilenames = [i for i in glob.glob(datadir)]
all_querryfilenames = [i for i in glob.glob(querrydir)]

#gravando quantidade de elementos nos arrays
td = len(all_datafilenames)
tq = len(all_querryfilenames)

count = {}
org_count = {}

def tokenizar_total (dataset):
    dk = 0
    #abrindo cada arquivo
    for i in dataset:
        #abrindo cada arquivo com leitura binária (rb)
        with open(i, 'rb') as file:
            #tokenizando elementos com nltk e regex 
            # (r) encaminha o termo que o segue para ser interpretado pela função sem ignorar a \ 
            # \w identifica palavras
            # + considera 1 ou mais  (remove espaços) 
            tokenizer = nltk.RegexpTokenizer(r"\w+")
            #tokenizando os elementos
            wtoken = tokenizer.tokenize(file.read().decode('ansi').lower())

            #Efetuando a exclusão das StopWords do dcumento já tokenizado
            wtoken = [p for p in wtoken if p not in stopwordnltk]
            
            #adicionando palavras tokenizadas ao vetor de Tokens
            global_words_Token.extend(wtoken)

            file.close()
    
            #dk += 1
            #print(str((int(dk)/int(tq))*100) + " %")
    return

def histogramar(text):
    
    #Variavel de vetor Chave:Valor
    tdt = len(text)
    dk = 0
    #efetua a contagem dos elementos
    #Para cada elemento no texto:
    for w in text:
        
        # se o elemento está no texto:
        if w in text:

            #Se o elemento ainda não foi contabilizado, ou seja não faz parte de count:
            if w not in count.keys():
                #O count do elemento recebe 1
                count[w] = 1
            else:
                #caso o elemento ja exista na chave count então soma-se 1 
                count[w] += 1
            
            #dk += 1
            #print(str((int(dk)/int(tdt))*100) + " %")
    #print (count)
    limiter = len(count)
    #Ordenação de elementos por aparição
    #função heapq.nlargest(Qtd de elementos a retornar, conjunto de iteração, Key que será gravada)
    freq_words = heapq.nlargest(limiter, count, key=count.get) 
    
    
    for w in freq_words:
        org_count[w] = count.get(w)
    

    
    return freq_words


tokenizar_total (all_querryfilenames)
dk = 0
histogramar (global_words_Token)
dk = 0
elementos_media = [a for a in list(org_count.values()) if a != 1]
print (sta.mean(elementos_media))
print(org_count)





def scoremaker (dataset):
    dk = 0
    #abrindo cada arquivo
    for i in dataset:

        #coletando nome do arquivo(filename) e diretório(path) 
        filename = i.split("\\")[-1].split(".")[0]
        path = i.split("\\")[-2]

        #Encaminhando o documento i para a função de tokenização, que remove pontuações, espaços e quebras de linha e separa os elementos
        words = tokenizar(i)

        #Efetuando a exclusão das StopWords do dcumento já tokenizado
        #clean_words = [p for p in words if p not in stopwordnltk]

        #As palavras já sem stopwords são encaminhadas para a função que contabiliza sua frequência e organiza o vetor por ordem da frequência obtida
        #organized = histogramar(clean_words)
        
        #nesse ponto são encaminhadas os elementos já tratados, juntamente ao conjunto de elementos totais do documento (excluindo pontuações, espaços e quebras de linha)
        #idf_result = idf(organized, words)
        #tf_result = tf(organized, words)

        #encaminha o resultado obtido pelas funções de tf e idf para criar o score de relevância dos termos para o documento
        #tf_idf = idftf(tf_result, idf_result)

        #gravacsv(filename, path, organized, tf_result, idf_result, tf_idf)

        #print (tf_result)
        #print (idf_result)
        #print (organized)
        dk += 1
        print(str((int(dk)/int(tq))*100) + " %")

def tokenizar (text):
    #abrindo cada arquivo com leitura binária (rb)
    with open(text, 'rb') as file:
        #tokenizando elementos com nltk e regex 
        # (r) encaminha o termo que o segue para ser interpretado pela função sem ignorar a \ 
        # \w identifica palavras
        # + considera 1 ou mais  (remove espaços) 
        tokenizer = nltk.RegexpTokenizer(r"\w+")
        #tokenizando os elementos
        wtoken = tokenizer.tokenize(file.read().decode('ansi').lower())
    
    return



def idf(dataidf,dataset):
    
    word_idfs = {}

    for wordd in dataidf:
        
        doc_count = 0
        
        for w in dataset:
            if w in dataidf:
                doc_count += 1
        word_idfs[wordd] = np.log((len(dataset)/doc_count)+1)
    return word_idfs

def tf (datatf, dataset):
    
    tf_matrix = {}
    
    for wordt in datatf:
        doc_tf = []    
        frequency = 0
        for w in dataset:
            if w == wordt:
                frequency += 1
        tf_word = frequency/len(datatf)
        doc_tf.append(tf_word)
        tf_matrix[wordt] = doc_tf

    return tf_matrix

def idftf (tf, idf):

    tfidf_matrix = []

    for wordtd in tf.keys():
        tfidf = []
        for value in tf[wordtd]:
            score = value * idf[wordtd]
            tfidf.append(score)
        
        #tfidf_matrix[wordtd] = tfidf
        tfidf_matrix.append(tfidf)

    return tfidf_matrix

def gravacsv (id, path, word, tf, idf, score):
    
    for i in word:
        
        with open(i, newline="\n") as csvfile:
            listaG = []
            arquivo_saida ='score_list.csv'
            listaG.append([id, path, word, tf.key(), idf.key(), score])
        
        with open(arquivo_saida, "w") as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=";", quoting=csv.QUOTE_MINIMAL)
            for i in listaG:
                spamwriter.writerow(i)
        csvfile.close()


#tokenizar_total (all_datafilenames)

#scoremaker (all_querryfilenames)


#print (org_count)