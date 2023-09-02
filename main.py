from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
import os
import database as db

template_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
template_dir = os.path.join(template_dir, 'src', 'templates')

app = Flask(__name__, template_folder = template_dir)




#Rutas de la aplicación
@app.route('/')
def home(): return render_template('index.html')

# #Ruta para guardar usuarios en la bdd
# @app.route('/user', methods=['POST'])
# def addUser():
#     username = request.form['username']
#     name = request.form['name']
#     password = request.form['password']

#     if username and name and password:
#         cursor = db.database.cursor()
#         sql = "INSERT INTO users (username, name, password) VALUES (%s, %s, %s)"
#         data = (username, name, password)
#         cursor.execute(sql, data)
#         db.database.commit()
#     return redirect(url_for('home'))

# @app.route('/delete/<string:id>')
# def delete(id):
#     cursor = db.database.cursor()
#     sql = "DELETE FROM users WHERE id=%s"
#     data = (id,)
#     cursor.execute(sql, data)
#     db.database.commit()
#     return redirect(url_for('home'))

# @app.route('/edit/<string:id>', methods=['POST'])
# def edit(id):
#     username = request.form['username']
#     name = request.form['name']
#     password = request.form['password']

#     if username and name and password:
#         cursor = db.database.cursor()
#         sql = "UPDATE users SET username = %s, name = %s, password = %s WHERE id = %s"
#         data = (username, name, password, id)
#         cursor.execute(sql, data)
#         db.database.commit()
#     return redirect(url_for('home'))

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




@app.route('/persona_add', methods=['POST'])
def persona_add():
    nombre = request.form['nombre']
    t_doc = request.form['t_doc']
    n_doc = int(request.form['n_doc'])
    nacimiento = datetime.strptime(request.form['nacimiento'], '%Y-%m-%d').date()
    print( request.form['sexo'])
    sexo = request.form['sexo']
    tel_cel = request.form.get('tel_cel')
    vivienda_actual =  int(request.form['vivienda_actual'])
    if all(x for x in request.form.values()):
        cursor = db.database.cursor()
        sql = "INSERT INTO personas (id, tipo_doc, nombre, fecha_nac,  sexo, telefono, id_vivienda_actual) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        data= (n_doc, t_doc, nombre, nacimiento, sexo, tel_cel, vivienda_actual)
        cursor.execute(sql, data)
        db.database.commit()
    return redirect(url_for('persona'))



@app.route('/persona_edit/<string:id>', methods=["POST"])
def persona_edit(id):
    print('ID DE PERSONA: --> ', id)
    new_id = request.form['id']
    tipo_doc = request.form['tipo_doc']
    nombre = request.form['nombre']
    fecha_nac = request.form['fecha_nac']
    sexo = request.form['sexo']
    telefono = request.form['telefono']
    vivienda_actual = request.form['vivienda_actual']

    if all(x for x in request.form.values() if x not in {'telefono'}): #Telefono puede ser Null
        cursor = db.database.cursor()
        sql = "UPDATE personas SET id = %s, tipo_doc = %s, nombre = %s, fecha_nac = %s, sexo = %s, telefono=%s, id_vivienda_actual = %s WHERE id = %s"
        data = (new_id, tipo_doc, nombre, fecha_nac, sexo, telefono,vivienda_actual, id)
        cursor.execute(sql, data)
        db.database.commit()
    return redirect(url_for('persona'))


@app.route('/persona_delete/<string:id>')
def persona_delete(id):
    cursor = db.database.cursor()
    sql = "DELETE FROM personas WHERE id=%s"
    data = (id,)
    cursor.execute(sql, data)
    db.database.commit()
    return redirect(url_for('persona'))
 

@app.route('/vivienda')
def vivienda():
    cursor = db.database.cursor()
    cursor.execute("SELECT * FROM viviendas")
    myresult = cursor.fetchall()
    #Convertir los datos a diccionario
    insertObject = []
    columnNames = [column[0] for column in cursor.description]
    for record in myresult:
        print(record)
        insertObject.append(dict(zip(columnNames,record)))
    cursor.close()
    
    return render_template('vivienda.html', data=insertObject)
@app.route('/vivienda_add', methods=['POST'])
def vivienda_add():
    direccion = request.form['direccion']
    id_municipio = int(request.form['id_municipio'])
    capacidad = int(request.form['capacidad'])
    niveles = int(request.form['niveles'])
    if all(x for x in request.form.values()):
        cursor = db.database.cursor()
        sql = "INSERT INTO viviendas (direccion, id_municipio, capacidad,  niveles) VALUES (%s, %s, %s, %s)"
        data= (direccion, id_municipio, capacidad, niveles)
        cursor.execute(sql, data)
        db.database.commit()
    return redirect(url_for('vivienda'))

@app.route('/vivienda_edit/<string:id>', methods=['POST'])
def vivienda_edit(id):
    direccion = request.form['direccion']
    id_municipio = int(request.form['id_municipio'])
    capacidad = int(request.form['capacidad'])
    niveles = int(request.form['niveles'])

    if all(x for x in request.form.values()):
        cursor = db.database.cursor()
        sql = "UPDATE viviendas SET direccion = %s, id_municipio = %s, capacidad = %s, niveles = %s WHERE id = %s"
        data = (direccion, id_municipio, capacidad, niveles, id)
        cursor.execute(sql, data)
        db.database.commit()
    return redirect(url_for('vivienda'))



@app.route('/vivienda_delete/<string:id>')
def vivienda_delete(id):
    cursor = db.database.cursor()
    sql = "DELETE FROM viviendas WHERE id=%s"
    data = (id,)
    cursor.execute(sql, data)
    db.database.commit()
    return redirect(url_for('vivienda'))



@app.route('/municipio')
def municipio():
    cursor = db.database.cursor()
    cursor.execute("SELECT * FROM municipios")
    myresult = cursor.fetchall()
    #Convertir los datos a diccionario
    insertObject = []
    columnNames = [column[0] for column in cursor.description]
    for record in myresult:
        insertObject.append(dict(zip(columnNames, record)))
    cursor.close()
    
    return render_template('municipio.html', data=insertObject)

@app.route('/municipio_add', methods=['POST'])
def municipio_add():
    id = int(request.form['id'])
    nombre = request.form['nombre']
    if all(x for x in request.form.values()):
        cursor = db.database.cursor()
        sql = "INSERT INTO municipios (id, nombre) VALUES (%s, %s)"
        data= (id,nombre)
        cursor.execute(sql, data)
        db.database.commit()
    return redirect(url_for('municipio'))
    
    
@app.route('/municipio_edit/<string:id>', methods=['POST'])
def municipio_edit(id):
    new_id = int(request.form['id'])
    nombre = request.form['nombre']

    if all(x for x in request.form.values()):
        cursor = db.database.cursor()
        sql = "UPDATE municipios SET id = %s, nombre = %s WHERE id = %s"
        data = (new_id, nombre, id)
        cursor.execute(sql, data)
        db.database.commit()
    return redirect(url_for('municipio'))


@app.route('/municipio_delete/<string:id>')
def municipio_delete(id):
    cursor = db.database.cursor()
    sql = "DELETE FROM municipios WHERE id=%s"
    data = (id,)
    cursor.execute(sql, data)
    db.database.commit()
    return redirect(url_for('municipio'))



@app.route('/posesiones/<string:id>', methods=["GET"])
def posesiones(id):
    try:
        cursor = db.database.cursor()
        q="SELECT * FROM posesiones WHERE id_persona=%s"
        data=(id,)
        cursor.execute(q, data)
        myresult = cursor.fetchall()
    except:
        return render_template('index.html')
    #Convertir los datos a diccionario
    insertObject = []
    columnNames = [column[0] for column in cursor.description]
    for record in myresult:
        insertObject.append(dict(zip(columnNames, record)))
    cursor.close()
    
    return render_template('posesion.html', data=insertObject, id=id)

@app.route('/posesiones_add', methods=['POST'])
def posesiones_add():
    id_persona = int(request.form['id_persona'])
    id_vivienda = int(request.form['id_vivienda'])
    fecha_posesion =  datetime.now().strftime('%Y-%m-%d')
    try:
        if all(x for x in request.form.values()):
            cursor = db.database.cursor()
            sql = "INSERT INTO posesiones (id_persona, id_vivienda, fecha_posesion) VALUES (%s, %s, %s)"
            data= (id_persona,id_vivienda, fecha_posesion)
            cursor.execute(sql, data)
            db.database.commit()
    except:
        redirect(url_for('posesiones', id=id_persona))
    return redirect(url_for('posesiones', id=id_persona))


    
@app.route('/posesiones_edit/<string:id>', methods=['POST'])
def posesiones_edit(id):
    id_persona = int(request.form['id_persona'])
    id_vivienda = int(request.form['id_vivienda'])
    fecha_posesion = datetime.strptime(request.form['fecha_posesion'], '%Y-%m-%d').date()
    if all(x for x in request.form.values()):
        cursor = db.database.cursor()
        sql = "UPDATE posesiones SET id_persona = %s, id_vivienda = %s, fecha_posesion = %s WHERE id = %s"
        data = (id_persona, id_vivienda, fecha_posesion, id)
        cursor.execute(sql, data)
        db.database.commit()
    return redirect(url_for('posesiones', id= id_persona))



@app.route('/posesiones_delete/<string:id>/<string:id_p>')
def posesiones_delete(id, id_p):
    cursor = db.database.cursor()
    sql = "DELETE FROM posesiones WHERE id=%s"
    data = (id,)
    cursor.execute(sql, data)
    db.database.commit()
    return redirect(url_for('posesiones', id= id_p))


@app.route('/cdf/<string:id>', methods=["GET"])
def cdf(id):
    print('ESTA ES LA ID CDF: ---> ',  id)
    try:
        cursor = db.database.cursor()
        q="SELECT cdf.*, persona1.nombre AS nombre_persona1, persona2.nombre AS nombre_persona2 FROM cdf LEFT JOIN personas AS persona1 ON cdf.id_persona = persona1.id LEFT JOIN personas AS persona2 ON cdf.id_cdf = persona2.id WHERE cdf.id_persona =%s OR cdf.id_cdf =%s;"
        data=(id,id)
        cursor.execute(q, data)
        myresult = cursor.fetchall()
        
    except Exception as e:
        print('ERROR SQL: ---> ', e)
        return render_template('index.html')
            
    #Convertir los datos a diccionario
    insertObject = []
    
    columnNames = [column[0] for column in cursor.description]
    for record in myresult:
        insertObject.append(dict(zip(columnNames, record)))
    cursor.close()
    data_pred= {'id': id}
    return render_template('cdf.html', data=insertObject, data_pred=data_pred)

@app.route('/cdf_add', methods=['POST'])
def cdf_add():
    id_persona = int(request.form['id_persona'])
    id_vivienda = int(request.form['id_cdf'])
    fecha_registro =  datetime.now().strftime('%Y-%m-%d')
    try:
            
        if all(x for x in request.form.values()):
            cursor = db.database.cursor()
            sql = "INSERT INTO cdf (id_persona, id_cdf, fecha_registro) VALUES (%s, %s, %s)"
            data= (id_persona,id_vivienda, fecha_registro)
            cursor.execute(sql, data)
            db.database.commit()
    except:
        pass
    return redirect(url_for('cdf', id=id_persona))

fecha_actual = datetime.now().strftime('%Y-%m-%d')



@app.route('/cdf_edit/<string:id>', methods=['POST'])
def cdf_edit(id):
    id_persona = request.form['id_persona']
    id_vivienda = request.form['id_cdf']
    fecha_registro = datetime.strptime(request.form['fecha_registro'], '%Y-%m-%d').date()
    try:
        if all(x for x in request.form.values()):
            cursor = db.database.cursor()
            sql = "UPDATE cdf SET id_persona = %s, id_cdf = %s, fecha_registro = %s WHERE id = %s"
            data = (id_persona, id_vivienda, fecha_registro, id)
            cursor.execute(sql, data)
            db.database.commit()
    except:
        return redirect(url_for('cdf', id=id))
    return redirect(url_for('cdf', id=id_persona))


@app.route('/cdf_delete/<string:id_r>/<string:id_p>')
def cdf_delete(id_r, id_p):
    cursor = db.database.cursor()
    sql = "DELETE FROM cdf WHERE id=%s"
    data = (id_r,)
    cursor.execute(sql, data)
    db.database.commit()
    return redirect(url_for('cdf', id=id_p))

if __name__ == '__main__':
  app.run(port=5000)
