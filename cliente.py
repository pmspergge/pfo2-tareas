import requests

API_URL = "http://127.0.0.1:5000"

def registrar(usuario, contrasena):
    r = requests.post(f"{API_URL}/registro", json={"usuario": usuario, "contraseña": contrasena})
    print("Registro:", r.status_code, r.json())

def login(session, usuario, contrasena):
    r = session.post(f"{API_URL}/login", json={"usuario": usuario, "contraseña": contrasena})
    print("Login:", r.status_code, r.json())

def ver_tareas(session):
    r = session.get(f"{API_URL}/tareas")
    print("Tareas HTML:\n", r.text)

def agregar_tarea(session, descripcion):
    r = session.post(f"{API_URL}/tareas", json={"descripcion": descripcion})
    print("Agregar tarea:", r.status_code, r.json())

if __name__ == "__main__":
    usuario = "testuser"
    contrasena = "test1234"

    # Registro
    registrar(usuario, contrasena)

    # Login y ver tareas
    with requests.Session() as s:
        login(s, usuario, contrasena)
        agregar_tarea(s, "Mi primera tarea")
        ver_tareas(s)