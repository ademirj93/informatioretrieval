import glob
from os import sep
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
nltk.download('stopwords')
nltk.download('punkt')
import csv
import re

stopwordnltk = stopwords.words('english')
dir ="./dataset/newdata/" 
td = 0
dk = 0
#dirglob = "./dataset/**/*"
dirglob = "./Dataset_test/*"
dirtyelem =['<']

all_filenames = [i for i in glob.glob(dirglob)]
td = len(all_filenames)



def removestopwords(texto):
    base =[]
    for (text) in texto:
        clean = [p for p in text.split() if p not in stopwordnltk]
        base.extend(clean)
    return base

for i in all_filenames:
    content = []
    words = []

    with open(i, newline="\n") as csvfile:
        
        listaG = []
        for elem in csvfile:
            temp = elem.lower().strip().split(" ")
            content.extend(temp)
            for w in temp:
                words.append(re.sub('[^@\w]','',w))
            

        spamreader = csv.reader (content, delimiter=",", quotechar='|')

        
        filename = i.split("\\")[-1].split(".")[0]
        path = i.split("\\")[-2]

        listaG.append(','.join(content)) 
        #arquivo_saida = dir + filename +'.csv'
        csvfile.close()
        dk += 1

    print(str((int(dk)/int(td))*100) + " %")

words = word_tokenize(' '.join(words))

tokenized = []
for row in words:
    for sent in sent_tokenize(row):
        for token in word_tokenize(sent):
            print (token)
            tokenized.append(token)
            
print (tokenized)
