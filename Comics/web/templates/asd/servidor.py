# Maximiliano da silva, grupo 18: comics, Servidor V1.1
from flask import Flask, request, jsonify, render_template
from Comics.Servicios.Autentificacion import autenticacion

app = Flask(__name__)


# El frontend servidor le envía un un request con los datos del html a autentificación, la cual lo transforma en un
# JSON que lo envía al backend del servidor a la función que corresponda para que lo procese.

# //////////////////////////////////////////////////////USUARIOS////////////////////////////////////////////////////////
# ------------------------------------------------------USUARIO|LOGIN---------------------------------------------------
@app.route('/', methods=['GET', 'POST'])
def login():
    return render_template('pagina.html')



# ------------------------------------------------------USUARIO|CREAR---------------------------------------------------
@app.route('/usuarios', methods=['POST'])
def crear_usuario():
    datos_usuario = request.get_json()
    if 'nombre' not in datos_usuario:
        return 'El nombre de usuario es requerido', 412
    if 'contraseña' not in datos_usuario:
        return 'La contraseña es requerida', 412
    if 'contraseña' not in datos_usuario:
        return 'La contraseña es requerida', 412
    if 'contenidoExplicito' not in datos_usuario:
        datos_usuario['contenidoExplicito'] = '0'
    if 'rol' not in datos_usuario:
        datos_usuario['rol'] = 'Usuario'

    try:
        autenticacion.crear_usuario(datos_usuario['nombre'],
                                    datos_usuario['contraseña'],
                                    datos_usuario['email'],
                                    datos_usuario['contenidoExplicito'],
                                    datos_usuario['rol']
                                    )
        return 'OK', 200
    except:
        return "ERROR DE CONFLICTO: NOMBRE DE USUARIO DEBE SER ÚNICO", 409


# ------------------------------------------------------USUARIO|PEDIR---------------------------------------------------
@app.route('/usuarios/<int:usuarioID>', methods=['GET'])
def pedir_usuario(usuarioID):
    respuesta = autenticacion.pedir_usuario(usuarioID)
    return respuesta


# ------------------------------------------------------USUARIO|BUSCAR--------------------------------------------------
@app.route('/usuarios', methods=['GET'])
def buscar_usuario():
    datos = request.get_json()

    try:
        respuesta = autenticacion.buscar_usuarios(
            datos['columna'],
            datos['buscar']
        )
        return respuesta
    except Exception as e:
        return e


# ------------------------------------------------------USUARIO|EDITAR--------------------------------------------------
@app.route('/usuarios/<int:usuarioID>', methods=['PUT'])
def editar_usuario(usuarioID):
    datos_editar = request.get_json()

    if 'nombre' not in datos_editar:
        return 'El nombre de usuario es requerido', 412

    if 'contraseña' not in datos_editar:
        return 'La contraseña es requerida', 412

    if 'rol' not in datos_editar:
        return 'El rol es requerido', 412

    if 'email' not in datos_editar:
        return 'El email es requerido', 412

    if 'contenidoExplicito' not in datos_editar:
        return 'El contenido explicito es requerido', 412

    respuesta = autenticacion.editar_usuario(usuarioID,
                                             datos_editar['nombre'],
                                             datos_editar['contraseña'],
                                             datos_editar['contenidoExplicito'],
                                             datos_editar['email'],
                                             datos_editar['rol']
                                             )
    return respuesta


# ------------------------------------------------------USUARIO|ELIMINAR------------------------------------------------
@app.route('/usuarios/<int:usuarioID>', methods=['DELETE'])
def eliminar_usuario(usuarioID):
    respuesta = autenticacion.eliminar_usuario(usuarioID)
    return respuesta


# //////////////////////////////////////////////////////COMICS//////////////////////////////////////////////////////////
# ------------------------------------------------------COMIC|CREAR-----------------------------------------------------
@app.route('/comics', methods=['POST'])
def crear_comic():
    datos_comic = request.get_json()
    if 'nombre' not in datos_comic:
        return 'El nombre de comic es requerido', 412

    if 'genero' not in datos_comic:
        return 'El genero es requerido', 412

    if 'autor' not in datos_comic:
        return 'El autor es requerido', 412

    if 'idioma' not in datos_comic:
        return 'El idioma es requerido', 412

    if 'ultimaEmision' not in datos_comic:
        return 'La ultima emision es requerida', 412

    if 'ultimoCapitulo' not in datos_comic:
        return 'El ultimo capitulo es requerido', 412

    if 'estado' not in datos_comic:
        return 'El estado es requerido', 412

    if 'pagina' not in datos_comic:
        return 'La pagina es requerida', 412

    if 'URL' not in datos_comic:
        return 'La URL es requerida', 412
    try:
        autenticacion.crear_comic(datos_comic['nombre'],
                                  datos_comic['genero'],
                                  datos_comic['autor'],
                                  datos_comic['idioma'],
                                  datos_comic['ultimaEmision'],
                                  datos_comic['ultimoCapitulo'],
                                  datos_comic['estado'],
                                  datos_comic['pagina'],
                                  datos_comic['rating'],
                                  datos_comic['URL']
                                  )
        return 'OK', 200
    except Exception as e:
        return "ERROR DE CONFLICTO: URL DEBE SER UNICA", 409


# ------------------------------------------------------COMIC|PEDIR-----------------------------------------------------
@app.route('/comics/<int:IDC>', methods=['GET'])
def pedir_comic(IDC):
    respuesta = autenticacion.pedir_comic(IDC)
    return respuesta


# ------------------------------------------------------COMIC|BUSCAR----------------------------------------------------

@app.route('/comics', methods=['GET'])
def buscar_comic():
    try:
        factor = request.get_json()
        respuesta = autenticacion.buscar_comic(
            factor['columna'],
            factor['buscar']
        )
        return respuesta
    except:
        return "ERROR DE SINTAXIS", 412


# ------------------------------------------------------COMIC|EDITAR----------------------------------------------------
@app.route('/comics/<int:IDC>', methods=['PUT'])
def editar_comic(IDC):
    datos_comic = request.get_json()
    try:
        respuesta = autenticacion.editar_comic(IDC,
                                               datos_comic['nombre'],
                                               datos_comic['genero'],
                                               datos_comic['autor'],
                                               datos_comic['idioma'],
                                               datos_comic['estado'],
                                               datos_comic['ultimaEmision'],
                                               datos_comic['ultimoCapitulo'],
                                               datos_comic['pagina'],
                                               datos_comic['rating']
                                               )
    except:
        return "ERROR DE SINTAXIS", 412

    return respuesta


# ------------------------------------------------------COMIC|ELIMINAR--------------------------------------------------
@app.route('/comics/<int:IDC>', methods=['DELETE'])
def eliminar_comic(IDC):
    respuesta = autenticacion.eliminar_comic(IDC)
    return respuesta


# //////////////////////////////////////////////////////LISTA///////////////////////////////////////////////////////////
# ------------------------------------------------------LISTA|CREAR-----------------------------------------------------
@app.route('/listas', methods=['POST'])
def crear_lista(usuarioID, IDC):
    if not usuarioID:
        return 'El ID del comic es requerido', 412
    if not IDC:
        return 'El ID del usuario es requerida', 412

    respuesta = autenticacion.crear_lista(usuarioID,
                                          IDC
                                          )
    return respuesta


# ------------------------------------------------------LISTA|PEDIR-----------------------------------------------------
@app.route('/listas/<int:listaID>', methods=['GET'])
def pedir_lista(listaID):
    respuesta = autenticacion.pedir_lista(listaID)
    return respuesta


# ------------------------------------------------------LISTA|BUSCAR----------------------------------------------------
@app.route('/listas', methods=['GET'])
def buscar_lista(factor):
    try:
        respuesta = autenticacion.buscar_lista(
            factor['columna'],
            factor['buscar']
        )
        return respuesta
    except:
        return "ERROR DE SINTAXIS", 412


# ------------------------------------------------------LISTA|EDITAR----------------------------------------------------
@app.route('/listas/<int:listaID>', methods=['PUT'])
def editar_lista(listaID):
    datos_lista = request.get_json()

    if 'IDC' not in datos_lista:
        return 'El ID del comic es requerido', 412
    if 'usuarioID' not in datos_lista:
        return 'El ID del usuario es requerido', 412

    respuesta = autenticacion.editar_lista(listaID,
                                           datos_lista['usuarioID'],
                                           datos_lista['IDC']
                                           )
    return respuesta


# ------------------------------------------------------LISTA|ELIMINAR--------------------------------------------------
@app.route('/listas/<int:listaID>', methods=['DELETE'])
def eliminar_lista(listaID):
    respuesta = autenticacion.eliminar_lista(listaID)

    return respuesta


# //////////////////////////////////////////////////////EJECUCIÓN///////////////////////////////////////////////////////
if __name__ == '__main__':
    app.debug = True
    app.run(port=5001)
