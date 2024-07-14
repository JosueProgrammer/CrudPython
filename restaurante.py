import sqlite3
from collections import defaultdict

def crear_bd():
    conn = sqlite3.connect('restaurante.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS categoria (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT UNIQUE NOT NULL
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS plato (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT UNIQUE NOT NULL,
        categoria_id INTEGER,
        precio REAL NOT NULL,
        FOREIGN KEY (categoria_id) REFERENCES categoria (id)
    )
    ''')
    
    conn.commit()
    conn.close()

def insertar_categoria(nombre):
    conn = sqlite3.connect('restaurante.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute('INSERT INTO categoria (nombre) VALUES (?)', (nombre,))
        conn.commit()
    except sqlite3.IntegrityError:
        return "La categoría ya existe."
    
    conn.close()
    return "Categoría agregada con éxito."

def insertar_plato(nombre, categoria_id, precio):
    conn = sqlite3.connect('restaurante.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute('INSERT INTO plato (nombre, categoria_id, precio) VALUES (?, ?, ?)', (nombre, categoria_id, precio))
        conn.commit()
    except sqlite3.IntegrityError:
        return "El plato ya existe."
    
    conn.close()
    return "Plato agregado con éxito."

def obtener_categorias():
    conn = sqlite3.connect('restaurante.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM categoria')
    categorias = cursor.fetchall()
    
    conn.close()
    return categorias

def obtener_platos():
    conn = sqlite3.connect('restaurante.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT p.id, p.nombre, c.nombre, p.precio FROM plato p JOIN categoria c ON p.categoria_id = c.id')
    platos = cursor.fetchall()
    
    conn.close()
    return platos

def eliminar_plato(id_plato):
    conn = sqlite3.connect('restaurante.db')
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM plato WHERE id=?', (id_plato,))
    conn.commit()
    
    conn.close()
    return "Plato eliminado con éxito."

def actualizar_plato(id_plato, nombre, categoria_id, precio):
    conn = sqlite3.connect('restaurante.db')
    cursor = conn.cursor()
    
    cursor.execute('UPDATE plato SET nombre=?, categoria_id=?, precio=? WHERE id=?', (nombre, categoria_id, precio, id_plato))
    conn.commit()
    
    conn.close()
    return "Plato actualizado con éxito."

def eliminar_categoria(id_categoria):
    conn = sqlite3.connect('restaurante.db')
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM categoria WHERE id=?', (id_categoria,))
    conn.commit()
    
    conn.close()
    return "Categoría eliminada con éxito."
def obtener_platos_por_categoria():
    conn = sqlite3.connect("restaurante.db")
    cursor = conn.cursor()
    cursor.execute("SELECT platos.nombre, categorias.nombre, platos.precio FROM platos INNER JOIN categorias ON platos.categoria_id = categorias.id ORDER BY categorias.nombre")
    platos_por_categoria = defaultdict(list)
    for nombre_plato, nombre_categoria, precio in cursor.fetchall():
        platos_por_categoria[nombre_categoria].append((nombre_plato, precio))
    conn.close()
    return platos_por_categoria


