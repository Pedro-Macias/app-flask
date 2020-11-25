# MINUTO 23.08


from flask import Flask
from flask import render_template
from flask import request
from flask_mysqldb import MySQL

app = Flask(__name__)

# conectarse a la base de datos
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'pedro'
app.config['MYSQL_PASSWORD'] = '123'
app.config['MYSQL_DB'] = 'contactos_flask'

mysql = MySQL(app)

# rutas de las paginas
@app.route('/')
def index ():
    return render_template('index.html')

@app.route('/agregar_contactos', methods = ['POST'])
def agregar_contactos ():
    if request.method == 'POST':
        nombre = request.form['nombre']
        telefono = request.form['telefono']
        email = request.form['email']
        print(nombre)
        print(telefono)
        print(email)
        #creamos un cursor a MYSQL
        cursor = mysql.connection.cursor()
        #escribimos la consulta que vamos a enviar
        cursor.execute('INSERT INTO contactos(nombre, telefono, email) VALUES (%s, %s, %s)',
        (nombre, telefono, email))
        # enviamos a la base de datos
        mysql.connection.commit()
        return 'recibido'


@app.route('/editar')
def editar():
    return 'editar contactos'

@app.route('/borrar')
def borrar():
    return ' borrar contactos'





if __name__ == '__main__':
    app.run(port = 3000, debug = True)
    # http://localhost:3000