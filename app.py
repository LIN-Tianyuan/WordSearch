from flask import Flask, render_template, request
import pymysql
app = Flask(__name__)

host = 'localhost'
user='root'
password=''
database='indexation'


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
    search_query = request.form['search_query']
    results = search_in_database(search_query)
    return render_template('search.html', results=results)

@app.route('/')
def index():
    return render_template('search.html')

if __name__ == '__main__':
    app.run(debug=True)