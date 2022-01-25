from Comics.Datos.modelos import usuario as modelo_usuario
from Comics.Datos.modelos import comic as modelo_comic
from Comics.Datos.modelos import lista as modelo_lista


# ///////////////////////////////////////////////////////////USUARIO////////////////////////////////////////////////////
def crear_usuario(nombre, contraseña, email, contenidoExplicito, rol):
    modelo_usuario.crear_usuario(nombre,
                                 contraseña,
                                 email,
                                 contenidoExplicito,
                                 rol
                                 )


def login_usuario(nombre, email, contraseña):
    try:
        respuesta = modelo_usuario.login_usuario(nombre,
                                                 email,
                                                 contraseña
                                                 )
        return respuesta
    except Exception as e:
        return print(e)


def eliminar_usuario(usuarioID):
    respuesta = modelo_usuario.eliminar_usuario(usuarioID)
    return respuesta


def editar_usuario(usuarioID, nombre, email, contraseña, contenidoExplicito, rol):
    respuesta = modelo_usuario.editar_usuario(usuarioID,
                                              nombre,
                                              email,
                                              contraseña,
                                              contenidoExplicito,
                                              rol
                                              )
    return respuesta


def pedir_usuario(usuarioID):
    respuesta = modelo_usuario.pedir_usuario(usuarioID)
    return respuesta


def buscar_usuarios(columna, buscar):
    try:
        respuesta = modelo_usuario.buscar_usuarios(columna,
                                                   buscar)
        return respuesta
    except Exception as e:
        return e

def fondo(metodo,nombre, fondo):
    resource = modelo_usuario.cambiar_fondo(metodo,
                                            nombre,
                                            fondo)
    return resource


# ///////////////////////////////////////////////////////////COMIC//////////////////////////////////////////////////////
def crear_comic(nombre, genero, autor, idioma, ultimaEmision, ultimoCapitulo, estado, pagina, rating, URL):
    modelo_comic.crear_comic(nombre,
                             genero,
                             autor,
                             idioma,
                             ultimaEmision,
                             ultimoCapitulo,
                             estado,
                             pagina,
                             rating,
                             URL)


def editar_comic(IDC, nombre, genero, autor, idioma, estado, ultimaEdicion,
                 ultimoCapitulo, pagina, rating):
    respuesta = modelo_comic.editar_comic(IDC,
                                          nombre,
                                          genero,
                                          autor,
                                          idioma,
                                          estado,
                                          ultimaEdicion,
                                          ultimoCapitulo,
                                          pagina,
                                          rating
                                          )
    return respuesta


def agregar_vista(IDC):
    respuesta = modelo_comic.agregar_vistas(IDC)
    return respuesta


def eliminar_comic(IDC):
    respuesta = modelo_comic.eliminar_comic(IDC)
    return respuesta


def pedir_comic(IDC):
    respuesta = modelo_comic.pedir_comic(IDC)
    return respuesta


def buscar_comic(columna, buscar):
    respuesta = modelo_comic.buscar_comic(columna,
                                          buscar
                                          )
    return respuesta


# ///////////////////////////////////////////////////////////LISTA//////////////////////////////////////////////////////
def mod_nombre_lista(usuarioID, nombre):
    respuesta = modelo_lista.modificar_nombre_lista(usuarioID,
                                                    nombre
                                                    )
    return respuesta

def crear_lista(usuarioID, IDC):
    respuesta = modelo_lista.crear_lista(usuarioID,
                                         IDC
                                         )
    return respuesta


def pedir_lista(listaID):
    respuesta = modelo_lista.pedir_lista(listaID)
    return respuesta


def buscar_lista(columna, buscar):
    respuesta = modelo_lista.buscar_lista(columna,
                                          buscar
                                          )
    return respuesta


def editar_lista(listaID, usuarioID, IDC):
    respuesta = modelo_lista.editar_lista(listaID,
                                          usuarioID,
                                          IDC
                                          )
    return respuesta


def eliminar_lista(listaID):
    respuesta = modelo_lista.eliminar_lista(listaID)
    return respuesta
