# PFO 2: Sistema de Gestión de Tareas

Este proyecto es una API RESTful desarrollada con Flask y SQLite para la gestión de usuarios y tareas, incluyendo autenticación segura y un cliente de consola para interactuar con la API.

## Instrucciones para ejecutar el proyecto

1. **Instala las dependencias:**

   ```bash
   pip install -r requirements.txt
   ```

2. **Ejecuta el servidor:**

   ```bash
   python servidor.py
   ```

3. **Prueba los endpoints:**
   - Registro de usuario: `POST /registro` con JSON `{ "usuario": "nombre", "contraseña": "1234" }`
   - Login: `POST /login` con JSON `{ "usuario": "nombre", "contraseña": "1234" }`
   - Ver tareas: `GET /tareas` (requiere sesión iniciada)

## Endpoints principales

| Método | Endpoint      | Descripción                        |
|--------|--------------|------------------------------------|
| POST   | /registro    | Registro de usuario                |
| POST   | /login       | Login de usuario                   |
| GET    | /tareas      | Ver tareas (HTML)                  |
| POST   | /tareas      | Agregar tarea                      |
| GET    | /usuarios    | Listar usuarios (solo pruebas)     |
| DELETE | /usuarios/<usuario> | Eliminar usuario (solo pruebas) |

## Notas
- Las contraseñas se almacenan hasheadas por seguridad.
- La base de datos utilizada es SQLite y se crea automáticamente al iniciar el servidor.

## Pruebas realizadas

- Registro de usuario exitoso y fallido (usuario existente)
- Login exitoso y fallido (contraseña incorrecta)
- Agregar tarea y visualización de tareas
- Acceso a tareas sin login (redirige o da error)

Ver capturas en el documento enlazado abajo.

## Respuestas conceptuales

**¿Por qué hashear contraseñas?**  
Hashear contraseñas protege la información de los usuarios en caso de filtración de la base de datos, ya que los hashes no pueden revertirse fácilmente a la contraseña original.

**Ventajas de usar SQLite:**  
- No requiere servidor adicional.
- Portabilidad y facilidad de uso.
- Ideal para proyectos pequeños y prototipos.

## Capturas de pantalla

Las capturas de todas las pruebas realizadas están disponibles en el siguiente documento de Google Docs:

[Enlace a las capturas](https://docs.google.com/document/d/1W86AUmeLJFwX8qJqzECOpcBrZTEZzJTPxo4johDs1aI/edit?usp=sharing)

---

**Autor:** Pedro Matias Spergge  
**Fecha de entrega:** 20/06/2025

