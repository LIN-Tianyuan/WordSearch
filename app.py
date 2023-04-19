from flask import Flask, render_template, request, redirect, url_for
import pymysql
import os
from indexation_in_database import *
app = Flask(__name__)
UPLOAD_FOLDER = './static/File'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

host = 'localhost'
user='root'
password=''
database='indexation'

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

def search_word(db, cursor, word):
    final_results = []
    no_result = []
    try:
        sql1 = "select id from word where word = %s"
        cursor.execute(sql1, word)
        result1 = cursor.fetchone()
        sql2 = "select * from word_document_frequency where wordId = %s"
        cursor.execute(sql2, result1[0])
        result2 = cursor.fetchall()
        print(result2)
        for result in result2:
            list = []
            document_id = result[1]
            sql3 = "select document, path from document where id = %s"
            cursor.execute(sql3, document_id)
            result3 = cursor.fetchall()
            list.append(word)
            list.append(result[2])
            list.append(result3[0][0])
            list.append(result3[0][1])
            final_results.append(list)
        print("Mot: " + word)
        print("ID du mot: " + str(result1[0]))
        print(final_results)
        print("Recherche réussie pour le mot id.")
        return final_results
    except:
        print("Échec de la recherche du mot id.")
        list = []
        list.append(word)
        no_result.append(list)
        db.rollback()
        return no_result
    finally:
        db.close()

def update_database():
    insert_alldata()

@app.route('/search', methods=['POST'])
def search():
    db, cursor = get_cursor()
    search_query = request.form['search_query']
    results = search_word(db, cursor, search_query)
    print(results)
    return render_template('search.html', results=results)

@app.route('/uploadFile', methods=['POST'])
def uploadFile():
    file = request.files['file']
    if file:
        filename = file.filename
        current_path = os.path.abspath(__file__)
        father_path = os.path.abspath(os.path.dirname(current_path) + os.path.sep + ".")
        file_path = father_path + "/static/File"
        file.save(os.path.join(file_path, filename))
        print("Le fichier a été téléchargé dans le dossier spécifié: " + file_path)
    update_database()
    return render_template('search.html')

@app.route('/')
def index():
    return render_template('search.html')

if __name__ == '__main__':
    app.run(debug=True)