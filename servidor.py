from flask import Flask, request, jsonify, session, redirect, url_for, render_template_string
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)
app.secret_key = 'supersecretkey'
DATABASE = 'tareas.db'

# --- Utilidades de base de datos ---
def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as db:
        db.execute('''CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE NOT NULL,
            contrasena TEXT NOT NULL
        )''')
        db.execute('''CREATE TABLE IF NOT EXISTS tareas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            descripcion TEXT NOT NULL,
            FOREIGN KEY(usuario_id) REFERENCES usuarios(id)
        )''')

# --- Endpoints ---
@app.route('/registro', methods=['POST'])
def registro():
    data = request.get_json()
    usuario = data.get('usuario')
    contrasena = data.get('contraseña')
    if not usuario or not contrasena:
        return jsonify({'error': 'Faltan datos'}), 400
    hash_contrasena = generate_password_hash(contrasena)
    try:
        with get_db() as db:
            db.execute('INSERT INTO usuarios (usuario, contrasena) VALUES (?, ?)', (usuario, hash_contrasena))
        return jsonify({'mensaje': 'Usuario registrado exitosamente'}), 201
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Usuario ya existe'}), 409

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    usuario = data.get('usuario')
    contrasena = data.get('contraseña')
    if not usuario or not contrasena:
        return jsonify({'error': 'Faltan datos'}), 400
    with get_db() as db:
        user = db.execute('SELECT * FROM usuarios WHERE usuario = ?', (usuario,)).fetchone()
        if user and check_password_hash(user['contrasena'], contrasena):
            session['usuario_id'] = user['id']
            return jsonify({'mensaje': 'Login exitoso'}), 200
        else:
            return jsonify({'error': 'Credenciales incorrectas'}), 401

@app.route('/tareas', methods=['GET'])
def tareas():
    if 'usuario_id' not in session:
        return redirect(url_for('login_html'))
    usuario_id = session['usuario_id']
    with get_db() as db:
        tareas = db.execute('SELECT descripcion FROM tareas WHERE usuario_id = ?', (usuario_id,)).fetchall()
    tareas_list = [t['descripcion'] for t in tareas]
    html = f"""
    <h1>Bienvenido/a</h1>
    <h2>Tus tareas:</h2>
    <ul>
        {''.join(f'<li>{t}</li>' for t in tareas_list)}
    </ul>
    """
    return render_template_string(html)

@app.route('/login', methods=['GET'])
def login_html():
    return '<h2>Por favor, inicia sesión usando POST /login</h2>'

@app.route('/usuarios', methods=['GET'])
def listar_usuarios():
    with get_db() as db:
        usuarios = db.execute('SELECT id, usuario FROM usuarios').fetchall()
    return jsonify([dict(u) for u in usuarios])

@app.route('/tareas', methods=['POST'])
def agregar_tarea():
    if 'usuario_id' not in session:
        return jsonify({'error': 'No autenticado'}), 401
    data = request.get_json()
    descripcion = data.get('descripcion')
    if not descripcion:
        return jsonify({'error': 'Falta la descripción'}), 400
    usuario_id = session['usuario_id']
    with get_db() as db:
        db.execute('INSERT INTO tareas (usuario_id, descripcion) VALUES (?, ?)', (usuario_id, descripcion))
    return jsonify({'mensaje': 'Tarea agregada exitosamente'}), 201

@app.route('/usuarios/<usuario>', methods=['DELETE'])
def borrar_usuario(usuario):
    with get_db() as db:
        result = db.execute('DELETE FROM usuarios WHERE usuario = ?', (usuario,))
        if result.rowcount == 0:
            return jsonify({'error': 'Usuario no encontrado'}), 404
    return jsonify({'mensaje': f'Usuario {usuario} eliminado exitosamente'}), 200

if __name__ == '__main__':
    init_db()
    app.run(debug=True) 