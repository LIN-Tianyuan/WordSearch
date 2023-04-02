import pymysql
from indexation import *

file = ['file.txt', 'file2.txt']
new_list = []
def fileList(file):
    for i in range(len(file)):
        freq = frequency(file[i])
        for key in freq.keys():
            tup = (key, freq[key], file[i])
            new_list.append(tup)
    return new_list

new_list = fileList(file)

host = 'localhost'
user='root'
password=''
database='indexation'

db = pymysql.connect(host=host,
                     user=user,
                     password=password,
                     database=database)
cursor = db.cursor()


try:
    sql = "insert into mot_frequence_doc(mot,freq,doc) values(%s, %s, %s)"
    cursor.executemany(sql, new_list)
    db.commit()
    print("Insérer les données avec succès")
except:
    print("Échec de l'insertion des données")
    db.rollback()

db.close()
