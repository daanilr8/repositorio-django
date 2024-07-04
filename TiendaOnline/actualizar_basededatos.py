import sqlite3
import os

# Función para actualizar un artículo
def actualizar_articulo(articulo_id,imagen_url):
    # Conectar a la base de datos
    base_path = 'D:\supra\Documents\git-repositorio\TiendaOnline'
    bd_path = 'db.sqlite3'
    file_path = os.path.join(base_path,bd_path)
    conn = sqlite3.connect(file_path)
    cur = conn.cursor()

    # Crear la consulta de actualización
    sql_update_query = '''
    UPDATE gestionPedidos_articulos
    SET imagen = ?
    WHERE id = ?
    '''

    # Ejecutar la consulta
    cur.execute(sql_update_query, (imagen_url, articulo_id))

    # Guardar los cambios
    conn.commit()

    # Confirmar cuántas filas fueron afectadas
    print(f'{cur.rowcount} fila(s) actualizada(s)')

    # Cerrar la conexión
    conn.close()

# Llamar a la función para actualizar un artículo
actualizar_articulo(8,'D:\supra\Documents\git-repositorio\TiendaOnline\media\BegoniasgeneradaIA.png')
actualizar_articulo(10,'D:\supra\Documents\git-repositorio\TiendaOnline\media\TulipangeneradaIA.png')
actualizar_articulo(13,'D:\supra\Documents\git-repositorio\TiendaOnline\media\ClavelesgeneradaIA.png')
actualizar_articulo(14,'D:\supra\Documents\git-repositorio\TiendaOnline\media\BuganvillageneradaIA.png')
actualizar_articulo(15,'D:\supra\Documents\git-repositorio\TiendaOnline\media\AmapolageneradaIA.png')