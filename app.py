from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'

# Conexión a la base de datos SQLite3
def conectar_bd():
    return sqlite3.connect('comentarios.db')

# Crear la tabla de usuarios y comentarios si no existen
def inicializar_bd():
    with conectar_bd() as conexion:
        with app.open_resource('schema.sql', mode='r') as f:
            conexion.cursor().executescript(f.read())
        conexion.commit()

# Ruta para iniciar sesión
@app.route('/inicio_sesion', methods=['GET', 'POST'])
def inicio_sesion():
    if request.method == 'POST':
        correo = request.form['correo']
        contrasena = request.form['contrasena']

        with conectar_bd() as conexion:
            cursor = conexion.cursor()
            cursor.execute('SELECT * FROM usuarios WHERE correo = ?', (correo,))
            usuario = cursor.fetchone()

            if usuario and check_password_hash(usuario[2], contrasena):
                session['usuario_id'] = usuario[0]
                return redirect(url_for('mostrar_comentarios'))

    return render_template('inicio_sesion.html')

# Ruta para cerrar sesión
@app.route('/cerrar_sesion')
def cerrar_sesion():
    session.pop('usuario_id', None)
    return redirect(url_for('inicio'))

# Ruta para mostrar comentarios existentes
@app.route('/contacto')
def mostrar_comentarios():
    with conectar_bd() as conexion:
        cursor = conexion.cursor()
        cursor.execute('SELECT nombre_usuario, comentario FROM comentarios JOIN usuarios ON comentarios.usuario_id = usuarios.id')
        comentarios = cursor.fetchall()

    return render_template('contacto.html', comentarios=comentarios)

# Ruta para guardar un nuevo comentario (requiere autenticación)
@app.route('/guardar_comentario', methods=['POST'])
def guardar_comentario():
    if 'usuario_id' in session:
        usuario_id = session['usuario_id']
        comentario_texto = request.form['comentario']

        with conectar_bd() as conexion:
            cursor = conexion.cursor()
            cursor.execute('INSERT INTO comentarios (usuario_id, comentario) VALUES (?, ?)',
                           (usuario_id, comentario_texto))
            conexion.commit()

    return redirect(url_for('mostrar_comentarios'))

# Ruta para registrar un nuevo usuario
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        correo = request.form['correo']
        contrasena = generate_password_hash(request.form['contrasena'])
        nombre_usuario = request.form['nombre_usuario']

        with conectar_bd() as conexion:
            cursor = conexion.cursor()
            cursor.execute('INSERT INTO usuarios (correo, contrasena, nombre_usuario) VALUES (?, ?, ?)',
                           (correo, contrasena, nombre_usuario))
            conexion.commit()

        # Después de registrarse, redirigir a la página de inicio de sesión
        return redirect(url_for('inicio_sesion'))

    return render_template('registro.html')

# Ruta para la página de inicio
@app.route('/')
def inicio():
    return render_template('index.html')

# Ruta para la página "Nosotros"
@app.route('/nosotros')
def nosotros():
    return render_template('nosotros.html')

# Ruta para la página "Servicios"
@app.route('/servicios')
def servicios():
    return render_template('servicios.html')

if __name__ == '__main__':
    inicializar_bd()
    app.run(debug=True)
