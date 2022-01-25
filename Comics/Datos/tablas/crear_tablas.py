import sqlite3

sql_tabla_usuarios = '''
CREATE TABLE USUARIO(
usuarioID INTEGER PRIMARY KEY AUTOINCREMENT,
nombre string not null UNIQUE,
email string not null,
contraseña string not null,
contenidoExplicito integer DEFAULT 0,
rol string
)
'''


sql_tablas_listas = '''
CREATE TABLE LISTA(
listaID integer PRIMARY KEY AUTOINCREMENT,
usuarioID integer,
usuario,
IDC integer,
nombreComic string,
FOREIGN KEY(usuario) REFERENCES USUARIO(usuarioID),
FOREIGN KEY(IDC) REFERENCES COMIC(IDC)
)
'''


sql_tabla_comics = '''
CREATE TABLE COMIC(
IDC INTEGER PRIMARY KEY AUTOINCREMENT,
nombre string not null,
genero string not null DEFAULT desconocido,
autor string not null DEFAULT desconocido,
idioma string not null DEFAULT desconocido,
estado string not null not null DEFAULT desconocido,
ultimaEmision string not null DEFAULT desconocido,
ultimoCapitulo string not null DEFAULT desconocido,
pagina string not null,
rating string not null DEFAULT desconocido,
URL string not null UNIQUE,
excplicito INTEGER
)
'''




if __name__ == '__main__':
    try:
        conexion = sqlite3.connect('E:\pythonProject2\Comics\Datos\comic.db')
        cursor = conexion.cursor()
        try:
            print('Borrando tabla antigua...')
            cursor.execute("DROP TABLE USUARIO")
            cursor.execute("DROP TABLE COMIC")
            cursor.execute("DROP TABLE LISTA")
        except Exception as a:
            print(f'Error BORRANDO base de datos: {a}')
        finally:
            print('Creando Tablas...')
            conexion.execute(sql_tablas_listas)
            conexion.execute(sql_tabla_usuarios)
            conexion.execute(sql_tabla_comics)
            conexion.close()
            print('Creacion Finalizada.')
        print('Terminamos.')
    except Exception as e:
        print(f'Error creando base de datos: {e}')
