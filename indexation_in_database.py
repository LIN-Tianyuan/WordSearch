import pymysql
from indexation import *

file = ['file.txt', 'file2.txt']
path = ['Web/static/File/file.txt', 'Web/static/File/file2.txt']
word_freq_doc = []
def fileList(file):
    new_list = []
    for i in range(len(file)):
        freq = frequency(file[i])
        for key in freq.keys():
            tup = (key, freq[key], file[i])
            new_list.append(tup)
    return new_list

new_list = fileList(file)
# Obtenir une liste de mots
def get_word_list(list):
    word_list = []
    for i in list:
        word_list.append(i[0])
    return word_list
# Obtenir une liste de documents
def get_document_list(file):
    document_list = []
    for i in range(len(file)):
        tup = (file[i], path[i])
        document_list.append(tup)
    return document_list

word_list = get_word_list(new_list)
document_list = get_document_list(file)

# Créer une connexion
def get_cursor():
    host = 'localhost'
    user = 'root'
    password = ''
    database = 'indexation'

    db = pymysql.connect(host=host,
                         user=user,
                         password=password,
                         database=database)
    cursor = db.cursor()
    return db, cursor

def insert_words(db, cursor):
    try:
        sql = "insert into word(word) values (%s)"
        cursor.executemany(sql, word_list)
        # cursor.executemany(sql2, document_list)
        db.commit()
        print("Insérer les mots avec succès.")
        print(word_list)
    except:
        print("Échec de l'insertion des mots.")
        db.rollback()
    finally:
        db.close()

def insert_documents(db, cursor):
    try:
        sql = "insert into document(document, path) value (%s, %s)"
        cursor.executemany(sql, document_list)
        # cursor.executemany(sql2, document_list)
        db.commit()
        print("Insérer les documents avec succès.")
        print(document_list)
    except:
        print("Échec de les documents des mots.")
        db.rollback()
    finally:
        db.close()

def insert_words_freqs_docs(db, cursor):
    try:
        for element in new_list:
            sql1 = "select id from word where word = %s"
            sql2 = "select id from document where document = %s"
            # str1 = "\"" + i[0] + "\""
            str1 = element[0]
            str2 = element[2]
            cursor.execute(sql2, str2)
            document = cursor.fetchone()[0]
            cursor.execute(sql1, str1)
            word = cursor.fetchone()[0]
            freq = element[1]
            tup = (word, document, freq)
            word_freq_doc.append(tup)
        sql = "insert into word_document_frequency(wordId, documentId, frequency) values(%s, %s, %s)"
        cursor.executemany(sql, word_freq_doc)
        db.commit()
        print("Insérer les données avec succès.")
        print(word_freq_doc)
    except:
        print("Échec de l'insertion des données.")
        db.rollback()
    finally:
        db.close()

def insert_alldata():
    db1, cursor1 = get_cursor()
    insert_words(db1, cursor1)
    db2, cursor2 = get_cursor()
    insert_documents(db2, cursor2)
    db3, cursor3 = get_cursor()
    insert_words_freqs_docs(db3, cursor3)

insert_alldata()
