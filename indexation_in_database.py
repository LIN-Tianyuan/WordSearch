import pymysql
from indexation import *
import os

filePath = '/Users/citron/Alex/Info/Univ/web/Web/static/File'
def get_file_and_path():
    files = []
    for i, j, k in os.walk(filePath):
        files = k
    return files

word_freq_doc = []
def fileList(file):
    new_list = []
    for i in range(len(file)):
        freq = frequency(file[i])
        for key in freq.keys():
            tup = (key, freq[key], file[i])
            new_list.append(tup)
    return new_list


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
        tup = (file[i], filePath)
        document_list.append(tup)
    return document_list

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
        word_list = get_word_list(fileList(get_file_and_path()))
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
        document_list = get_document_list(get_file_and_path())
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
        for element in fileList(get_file_and_path()):
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

def delete_database(db, cursor):
    try:
        sql1 = "delete from word"
        cursor.execute(sql1)
        sql2 = "delete from document"
        cursor.execute(sql2)
        sql3 = "delete from word_document_frequency"
        cursor.execute(sql3)
        # cursor.executemany(sql2, document_list)
        db.commit()
        print("Effacer les données avec succès.")
    except:
        print("Échec de la suppression des mots.")
        db.rollback()
    finally:
        db.close()

def insert_alldata():
    db1, cursor1 = get_cursor()
    delete_database(db1, cursor1)
    db2, cursor2 = get_cursor()
    insert_words(db2, cursor2)
    db3, cursor3 = get_cursor()
    insert_documents(db3, cursor3)
    db4, cursor4 = get_cursor()
    insert_words_freqs_docs(db4, cursor4)
