from flask import Flask, render_template, request, redirect, url_for
import os
import database as db


template_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
template_dir = os.path.join(template_dir, 'src', 'templates')

app = Flask(__name__, template_folder = template_dir)

@app.route('/')
def index():
  return render_template('index.html')


@app.route('/persona')
def persona():
    print('PETICION /persona !!')
    cursor = db.database.cursor()
    cursor.execute("SELECT * FROM personas")
    myresult = cursor.fetchall()
    #Convertir los datos a diccionario
    insertObject = []
    columnNames = [column[0] for column in cursor.description]
    for record in myresult:
        insertObject.append(dict(zip(columnNames,  [x if x!=None else " " for x in record])))
    cursor.close()
    return render_template('persona.html', data=insertObject)





if __name__ == '__main__':
  app.run(port=5000)
