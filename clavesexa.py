import sqlite3
import hashlib
from flask import Flask, request, render_template_string

# --- Configuración de Flask ---
app = Flask(__name__)

# --- Crear base de datos y tabla si no existen ---
def crear_db():
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS USER_PLAIN (
                    USERNAME TEXT PRIMARY KEY NOT NULL,
                    PASSWORD TEXT NOT NULL)''')
    conn.commit()
    conn.close()

# --- Función para hashear contraseñas ---
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# --- Guardar usuario con hash ---
def guardar_usuario(username, password):
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    c.execute("INSERT INTO USER_PLAIN (USERNAME, PASSWORD) VALUES (?, ?)",
              (username, hash_password(password)))
    conn.commit()
    conn.close()

# --- Verificar usuario con hash ---
def verificar_usuario(username, password):
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    c.execute("SELECT PASSWORD FROM USER_PLAIN WHERE USERNAME = ?", (username,))
    resultado = c.fetchone()
    conn.close()
    if resultado and resultado[0] == hash_password(password):
        return True
    return False

# --- Plantilla HTML simple ---
plantilla_html = '''
<!doctype html>
<title>Gestión de Usuarios</title>
<h2>Registrar nuevo usuario</h2>
<form method=post action="/registro">
  Usuario: <input type=text name=username required><br>
  Contraseña: <input type=password name=password required><br>
  <input type=submit value=Registrar>
</form>

<h2>Iniciar sesión</h2>
<form method=post action="/login">
  Usuario: <input type=text name=username required><br>
  Contraseña: <input type=password name=password required><br>
  <input type=submit value="Iniciar sesión">
</form>

<p>{{ mensaje }}</p>
'''

# --- Rutas Web ---
@app.route('/')
def inicio():
    return render_template_string(plantilla_html, mensaje='')

@app.route('/registro', methods=['POST'])
def registro():
    usuario = request.form['username']
    clave = request.form['password']
    try:
        guardar_usuario(usuario, clave)
        return render_template_string(plantilla_html, mensaje="✅ Usuario registrado.")
    except sqlite3.IntegrityError:
        return render_template_string(plantilla_html, mensaje="⚠️ El usuario ya existe.")

@app.route('/login', methods=['POST'])
def login():
    usuario = request.form['username']
    clave = request.form['password']
    if verificar_usuario(usuario, clave):
        return render_template_string(plantilla_html, mensaje="✅ Inicio de sesión exitoso.")
    else:
        return render_template_string(plantilla_html, mensaje="❌ Usuario o contraseña incorrecta.")

# --- Ejecutar App ---
if __name__ == '__main__':
    crear_db()
    app.run(host='0.0.0.0', port=7500, ssl_context='adhoc')
