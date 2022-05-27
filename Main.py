#import pandas as pd
import glob
from os import sep
import nltk as nl
import csv

dir ="./dataset/newdata/" 
td = 0
dk = 0

all_filenames = [i for i in glob.glob("./dataset/**/*")]
td = len(all_filenames)

for i in all_filenames:
    
    with open(i, newline="\n") as csvfile:
        
        content = []
        for elem in csvfile:
            content.extend(elem.strip().split("\n"))    

        spamreader = csv.reader (content, delimiter=";", quotechar='|')

        listaG = []
        filename = i.split("\\")[-1].split(".")[0]
        path = i.split("\\")[-2]

        listaG.append([filename, path, ','.join(content)]) 
        arquivo_saida = dir + filename +'.csv'
        csvfile.close()

    with open(arquivo_saida, "w") as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=";", quoting=csv.QUOTE_MINIMAL)
        for i in listaG:
            spamwriter.writerow(i)
        csvfile.close()

    dk += 1
    print(str((int(dk)/int(td))*100) + " %")

dk = 0
concatenar = [i for i in glob.glob("./dataset/newdata/*")]
td = len(concatenar)
listaf = []
header = ["id","path","content"]
with open("dataset.csv", "w") as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=";", quotechar='|')
    spamwriter.writerow(header)

for i in concatenar:

    with open(i, newline="") as csvfile:
        spamreader = csv.reader (csvfile, delimiter=";", quotechar='|')
        for row in spamreader:
            listaf.append([','.join(row)]) 
        csvfile.close()

    with open("dataset.csv", "w") as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=";", quoting=csv.QUOTE_MINIMAL)
        for i in listaf:    
            spamwriter.writerow(i)
        csvfile.close()

    dk += 1
    print(str((int(dk)/int(td))*100) + " %")