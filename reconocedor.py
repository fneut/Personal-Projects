import pandas as pd
import csv
import nltk
import numpy as np
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
import re
from sklearn.naive_bayes import GaussianNB
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn import preprocessing
from sklearn.feature_extraction.text import CountVectorizer
np.set_printoptions(threshold=np.inf)


def abonos_limpio(abono):
    if(pd.isnull(abono)):
        return ""
    else:
        return float(abono)

def cargos_limpio(cargo):
    if(pd.isnull(cargo)):
        return ""
    else:
        return float(cargo)

def label_movimientos(mov):
    if(pd.isnull(mov)):
        return 0
    else:
        return 1


def descripcion_limpio(desc): # a la parte derecha le saca las palabras "basuras" 
    if(desc.find(':') != -1 ):
        return " ".join([i for i in re.sub("[^a-zA-Z_]"," ",desc.split(":")[1]).split() if (i not in words and len(i)>1)]).lower()
    else:
        return " ".join([i for i in re.sub("[^a-zA-Z_]"," ",desc).split() if (i not in words)]).lower()

def transaccion_limpio(desc):
    if(desc.find(':') != -1 ):
        return " ".join([i for i in re.sub("[^a-zA-Z]"," ",desc.split(":")[0]).split()]).lower()
    else:
        desc = desc.lower() 
        list_de_categorias = desc.split(" ")
        for j in list_de_categorias:
            if(j in transac_pagos):
                return j
            elif(j in transac_recibos):
                return j
                       
 
predicciones = []

path = '/Users/fneut/Desktop/PP/SalidaData2.csv'
path2 = '/Users/fneut/Desktop/PP/set_categorias.csv'

df = pd.read_csv(path) #dataframe de cartola exportada
df2 = pd.read_csv(path2) #dataframe de categorías

stemmer = SnowballStemmer('spanish')
words = stopwords.words('spanish')
transac_pagos = ['pago', 'traspaso a', 'giro', 'pagos']
transac_recibos = ['traspaso de', 'retiro']


######################################### TEST DATA  ######################################### 


df['Des_limpio'] = df['Descripción'].apply(lambda x: descripcion_limpio(x)) 
df['Transaccion'] = df['Descripción'].apply(lambda x: transaccion_limpio(x)) 
df['Cargo_limpio'] = df['Cargos (CLP)'].apply(lambda x: cargos_limpio(x))
df['Abono_limpio'] = df['Abonos (CLP)'].apply(lambda x: abonos_limpio(x))
df['Saldo_limpio'] = df['Saldo (CLP)'].apply(lambda x: float(x))
df['movimiento'] = df['Cargos (CLP)'].apply(lambda x: label_movimientos(x))

df2['limpio'] = df2['Descripcion'].apply(lambda x: " ".join([i for i in re.sub("[^a-zA-Z]"," ",x).split() if (i not in words and len(i)>1)]).lower()) 
vectorizer = CountVectorizer() 

print(df)
print(df2)

vectorizer.fit(df2['limpio']) 
X_counts = vectorizer.fit_transform(df2['limpio']).toarray()
print("get features names: "+str(vectorizer.get_feature_names()) + '\n')
counts = vectorizer.transform(df2['limpio'])
print("printing count" + '\n' + str(counts.toarray()))


# ######### ASIGNAR LABELS A CATEGORIAS

le = preprocessing.LabelEncoder()
categoria_encoded=le.fit_transform(df2['Categoria'])

######################################### MODEL  ######################################### 

X_train = X_counts
gnb = GaussianNB()
gnb.fit(X_train,categoria_encoded)

######################################### TEST  ######################################### 

X_counts2 = vectorizer.transform(df['Des_limpio']).toarray()
predicted= gnb.predict(X_counts2) 

print("\n")
print("######################################### Input data: ######################################### " + "\n")
print(df[['Descripción','Cargos (CLP)','Abonos (CLP)','Saldo (CLP)']])

# print("######################################### Los cargos de entrada son: ######################################### " + "\n")
print("\n")
print("######################################### Resultado del modelo: ######################################### " + "\n")
for numero,x in enumerate(predicted):
    predicciones.append(list(le.classes_)[x])

df = df.assign(Categoria = predicciones)


with pd.option_context('display.max_rows', None):
    print(df[['Descripción','Cargos (CLP)','Abonos (CLP)','Saldo (CLP)','Categoria']])

#"""  


