from flask import Flask, render_template, request, redirect, url_for
import pymysql
import os

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
            sql3 = "select document from document where id = %s"
            cursor.execute(sql3, document_id)
            result3 = cursor.fetchall()
            list.append(word)
            list.append(result[2])
            list.append(result3[0][0])
            final_results.append(list)
        print("Mot: " + word)
        print("ID du mot: " + str(result1[0]))
        print(final_results)
        print("Recherche réussie pour le mot id.")
        return final_results
    except:
        print("Échec de la recherche du mot id.")
        db.rollback()
    finally:
        db.close()


def search_in_database(word):
    final_results = []
    db = pymysql.connect(host=host,
                         user=user,
                         password=password,
                         database=database)
    cursor = db.cursor()
    sql = "select * from mot_frequence_doc where mot = %s"
    try:
        # Exécution d'instructions SQL
        cursor.execute(sql, word)
        # Obtenir une liste de tous les enregistrements
        results = cursor.fetchall()
        for row in results:
            list = []
            word = row[0]
            frequency = row[1]
            document = row[2]
            list.append(word)
            list.append(frequency)
            list.append(document)
            final_results.append(list)
        return final_results
    except:
        print("Error: unable to fetch data")
    finally:
        # Fermer la connexion à la base de données
        db.close()


@app.route('/search', methods=['POST'])
def search():
    db, cursor = get_cursor()
    search_query = request.form['search_query']
    results = search_word(db, cursor, search_query)
    return render_template('search.html', results=results)

@app.route('/uploadFile', methods=['POST'])
def uploadFile():
    file = request.files['file']
    if file:
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('upload_file'))
    return render_template('search.html')

@app.route('/')
def index():
    return render_template('search.html')

if __name__ == '__main__':
    app.run(debug=True)