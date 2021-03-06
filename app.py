


from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import flash
from flask_mysqldb import MySQL

app = Flask(__name__)

# CONEXION a la base de datos MYSQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'pedro'
app.config['MYSQL_PASSWORD'] = '123'
app.config['MYSQL_DB'] = 'contactos_flask'

# INICIAR  una session 
app.secret_key = 'mysecretkey'

mysql = MySQL(app)

# rutas de las paginas
@app.route('/')
def index ():
    #conectamos con la base de datos . con el cursor
    cursor = mysql.connection.cursor()
    # le damos la orden , lo que queremos obtener
    cursor.execute('SELECT * FROM contactos')
    #ejecutamos la orden y obtenemos los datos , almacenandolos en una variable
    datos = cursor.fetchall()
    print(datos)
    return render_template('index.html', contactos = datos)

@app.route('/agregar_contactos', methods = ['POST'])
def agregar_contactos ():
    if request.method == 'POST':
        # recibimos los datos
        nombre = request.form['nombre']
        telefono = request.form['telefono']
        email = request.form['email']
        #creamos un cursor a MYSQL
        cursor = mysql.connection.cursor()
        #escribimos la consulta que vamos a enviar
        cursor.execute('INSERT INTO contactos(nombre, telefono, email) VALUES (%s, %s, %s)',
        (nombre, telefono, email))
        # enviamos a la base de datos
        mysql.connection.commit()
        # con flash , podemos enviar un mensaje
        flash('Contacto Agregado Satisfactoriamente')
        # lo redireccionarmos a la pagina principal una vez enviado el dato
        return redirect(url_for('index'))


@app.route('/editar/<string:id>')
def get_editar(id):
    # conectamos con la base de datos
    cursor = mysql.connection.cursor()
    # escribimos la consulta que queremos 
    cursor.execute('SELECT * FROM contactos WHERE id = %s',(id))
    # ejecuctamos la consulta , recibiendo la tupla
    dato = cursor.fetchall()
    return render_template('editar.html',contacto = dato[0])

@app.route('/actualizar/<string:id>', methods = ['POST'])
def actualizar(id):
    # si el metodo de envio es POST
    if request.method == 'POST':
        # recibimos todos los datos
        nombre = request.form['nombre']
        telefono = request.form['telefono']
        email = request.form['email']
        # conectamos con la base de datos
        cursor = mysql.connection.cursor()
        # la consulta que vamos a hacer en MYSQL
        cursor.execute('''
            UPDATE contactos 
            SET nombre = %s,
            telefono = %s, 
            email = %s 
            WHERE id = %s ''', (nombre, telefono, email, id))
        # ejecutamos la orden
        mysql.connection.commit()
        # enviamos un mensaje 
        flash('Contacto Actualizado')
        return redirect(url_for('index'))


# a la ruta borrar , le indicamos que recibe el parametro id
@app.route('/borrar/<string:id>')
def borrar(id):
    # nos conectamos a MYSQL
    cursor = mysql.connection.cursor()
    # ejecutamos la orden , que borre de la tabla la linea con el id que indicamos
    cursor.execute('DELETE FROM contactos WHERE id = {0}'.format(id))
    # enviamos a la base de datos para ejecutar
    mysql.connection.commit()
    # enviamos un mensaje
    flash('Contacto Eliminado Correctamente ')
    #redireccionamos a la pagina
    return redirect(url_for('index'))




if __name__ == '__main__':
    app.run(port = 3000, debug = True)
    # http://localhost:3000