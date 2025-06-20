import sqlite3

conn = sqlite3.connect('tareas.db')
cursor = conn.cursor()

for table in ['usuarios', 'tareas']:
    cursor.execute(f"PRAGMA table_info({table})")
    print(f"Estructura de la tabla {table}:")
    for row in cursor.fetchall():
        print(row)
    print()

conn.close()