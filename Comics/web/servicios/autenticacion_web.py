import requests
import Comics.web.servicios.rest_api as rest_api
import Comics.Datos.modelos.data as modelo_data


Ruta = rest_api.API_URL
Ruta2 = rest_api.API_URL_2


def fondo(metodo, nombre,fondo):
    try:
        if metodo == 'UPDATE':
            body = {"metodo": metodo,
                    "nombre": nombre,
                    "fondo": fondo}
            respuesta = requests.put(f'{Ruta}/usuarios/fondo', json=body)

            return respuesta.status_code == 200

        if metodo == 'GET':
            body = {"metodo": metodo,
                    "nombre": nombre,
                    "fondo": fondo}
            respuesta = requests.get(f'{Ruta}/usuarios/fondo', json=body)
            return respuesta

    except Exception as e:
        return e


def login(usuario, email, contraseña):
    try:
        body = {"nombre": usuario,
                "contraseña": contraseña,
                "email": email}

        respuesta = requests.post(f'{Ruta}/login', json=body)
        # Solo verificamos el code de la respuesta en este caso
        if respuesta.status_code == 200:
            return respuesta.status_code == 200

    except Exception as e:
        return e


def signup(usuario, email, contraseña):
    try:
        body = {"nombre": usuario,
                "contraseña": contraseña,
                "email": email,
                "contenidoExplicito": 0,
                "rol": "Usuario"}

        respuesta = requests.post(f'{Ruta}/usuarios', json=body)
        print("ok 200", respuesta)
        return respuesta.status_code == 200
    except Exception as e:
        print(e)
        return e


def usuarioID_con_nombre(nombre):
    body_usuario = {'columna': 'nombre', 'buscar': nombre}
    respuesta_usuario = requests.get(f'{Ruta}/usuarios', json=body_usuario)  # USE UN GET PARA BUSCAR USUARIO

    if respuesta_usuario.status_code == 404:
        print("NOT OK 404 en usuario con nombre")
        return respuesta_usuario

    respuesta_usuario = respuesta_usuario.json()
    if 'usuarioID' not in respuesta_usuario:
        usuarioID = respuesta_usuario['0']['usuarioID']
    else:
        usuarioID = respuesta_usuario['usuarioID']
    return usuarioID


def lista_con_nombre(nombre):
    body = {'columna': 'usuario', 'buscar': nombre}
    respuesta = requests.get(f'{Ruta}/listas', json=body)  # USE UN GET PARA BUSCAR USUARIO

    if respuesta.status_code == 404:
        print("NOT OK 404 en lista con nombre")
        return respuesta

    respuesta = respuesta.json()

    if 'listaID' not in respuesta:
        listaID = respuesta['0']['listaID']
    else:
        listaID = respuesta['listaID']

    return listaID


def lista_con_usuarioID(usuarioID):
    body = {'columna': 'usuarioID', 'buscar': usuarioID}
    respuesta = requests.get(f'{Ruta}/listas', json=body)  # USE UN GET PARA BUSCAR USUARIO

    if respuesta.status_code == 404:
        print("NOT OK 404 en usuario con nombre")
        return respuesta

    respuesta = respuesta.json()

    if 'listaID' not in respuesta:
        listaID = respuesta['0']['listaID']
    else:
        listaID = respuesta['listaID']

    return listaID


def lista_con_IDC(IDC):
    body = {'columna': 'IDC', 'buscar': IDC}
    respuesta = requests.get(f'{Ruta}/listas', json=body)  # USE UN GET PARA BUSCAR USUARIO

    if respuesta.status_code == 404:
        return respuesta

    respuesta = respuesta.json()

    if 'listaID' not in respuesta:
        listaID = respuesta['0']['listaID']
    else:
        listaID = respuesta['listaID']

    return listaID

def confirmar_nombre(nombre): # recibe un nombre y verifica que existe

    confirmacion = {'columna': 'nombre', 'buscar': nombre}
    respuest_confirmacion = requests.get(f'{Ruta}/usuarios',
                                         json=confirmacion)

    if respuest_confirmacion.status_code == 404:
        return "OK", 200
    else:
        return "ERROR DE CONTINGENCIA", 409


def modificar_usuario(usuario, nombre, email, contraseña, contenido):  # ACA SE VERIFICA QUE EL NOMBRE NO ESTE OCUPADO

    body_usuario = {'columna': 'nombre', 'buscar': usuario}
    respuesta_usuario = requests.get(f'{Ruta}/usuarios', json=body_usuario)  # USE UN GET PARA BUSCAR USUARIO
    respuesta_usuario = respuesta_usuario.json()

    if 'usuarioID' not in respuesta_usuario:
        rol = respuesta_usuario['0']['rol']
    else:
        rol = respuesta_usuario['rol']

    body = {"nombre": nombre,
            "email": email,
            "contraseña": contraseña,
            "contenidoExplicito": contenido,
            "rol": rol}

    usuarioID = usuarioID_con_nombre(usuario)

    respuesta_usuario = requests.put(f'{Ruta}/usuarios/{usuarioID}', json=body)

    if respuesta_usuario.status_code == 200:
        id = usuarioID_con_nombre(nombre)
        body_lista = {"nombre": nombre,
                      "usuarioID": id}

        requests.put(f'{Ruta}/listas/nombre', json=body_lista)
    return respuesta_usuario




def agregar_comic(url, usuario):
    # Aca busco el ID del usuario ya que lo necesito para crearle una lista
    usuarioID = usuarioID_con_nombre(usuario)

    # Aqui busco el IDC para mas adelante
    body_comic = {'columna': 'URL', 'buscar': url}
    respuesta_comic = requests.get(f'{Ruta}/comics', json=body_comic)  # USE UN GET PARA BUSCAR COMIC

    if respuesta_comic.status_code == 404:
        return respuesta_comic

    respuesta_comic = respuesta_comic.json()

    IDC = respuesta_comic['0']['IDC']

    # Aca creo la lista
    body_lista = {'usuarioID': usuarioID, 'IDC': IDC}
    respuesta_lista = requests.post(f'{Ruta}/listas', json=body_lista)  # USO POST PARA CREAR LISTA

    vista = {'IDC': IDC}
    requests.put(f'{Ruta}/comics/vistas', json=vista)  # USO PUT PARA AGREGAR UNA VISTA DEL COMIC

    if respuesta_lista.status_code == 200:
        return respuesta_lista

    if respuesta_lista.status_code == 404:
        return respuesta_lista
    if respuesta_lista.status_code == 409:
        return respuesta_lista


def obtener_usuarios(usuarioID):
    respuesta = requests.get(f'{Ruta}/usuarios/{usuarioID}')
    return respuesta.json()


def eliminar_usuario(nombre):
    usuarioID = usuarioID_con_nombre(nombre)
    listaID = lista_con_nombre(nombre)

    requests.delete(f'{Ruta}/usuarios/{usuarioID}')
    lista = requests.delete(f'{Ruta}/listas/{listaID}')

    while lista.status_code != 404:
        listaID = lista_con_nombre(nombre)
        lista = requests.delete(f'{Ruta}/listas/{listaID}')
    if usuarioID_con_nombre(nombre).status_code == 404 and lista_con_nombre(nombre).status_code == 404:
        print("termine")
        return "Usuario eliminado"


def buscar_usuario(columna, buscar):
    body = {"columna": columna,
            "buscar": buscar}
    respuesta = requests.get(f'{Ruta}/usuarios', json=body)
    return respuesta


def contenido_explicito(nombre):
    try:
        datos = buscar_usuario("nombre", nombre)
        datos = datos.json()
        respuesta = datos['contenidoExplicito']
        return respuesta
    except Exception as e:
        print(e)
        return e


def lista_usuario(usuario):
    body_lista = {'columna': 'usuario',
                  'buscar': usuario}
    # Este metodo envia un diccionario que jsonifique el cual tiene las tipicas key que señalizan cada comic
    respuesta_lista = requests.get(f'{Ruta}/listas', json=body_lista)

    if respuesta_lista.status_code == 404:
        return respuesta_lista

    respuesta_de_lista = respuesta_lista.json()
    respuesta = {}
    i = 0
    for comic in respuesta_de_lista.values():
        json = requests.get(f"{Ruta}/comics/{comic['IDC']}").json()
        respuesta[str(i)] = json
        i = i+1
    return respuesta


def lista_alterna(diccionarios):
    a = {}
    contador = 0
    if len(diccionarios) == 5:
        return lista_usuario(diccionarios['nombre'])
    else:
        for dato in diccionarios.values():
            a[contador] = dato['nombre']
            contador = contador + 1
    respuesta = {}
    contador = 0
    for i in a.values():  # estan los nombres
        lista = lista_usuario(i)
        if type(lista) == dict:
            for z in lista.values():
                respuesta[contador] = z
                contador = contador + 1
        else:
            respuesta[contador] = None
            contador = contador + 1
    return respuesta


def buscar_comics(columna, buscar):
    body = {"columna": columna,
            "buscar": buscar}

    respuesta = requests.get(f'{Ruta}/comics', json=body)

    if respuesta.status_code == 200:
        return respuesta
    else:
        return respuesta


def crear_comic(body):
    if type(body) != dict:
        return "ERROR DE TIPO", 500
    if buscar_comics('URL', body['URL']).status_code == 200:
        return "EL COMIC YA EXISTE", 409

    respuesta = requests.post(f'{Ruta}/comics', json=body)
    return respuesta


def eliminar_comic_simple(IDC):
    respuesta = requests.delete(f'{Ruta}/comics/{IDC}')

    listaID = lista_con_IDC(IDC)

    lista = requests.delete(f'{Ruta}/listas/{listaID}')

    while lista.status_code != 404:
        listaID = lista_con_IDC(IDC)
        lista = requests.delete(f'{Ruta}/listas/{listaID}')

    return respuesta


def eliminar_usuario_admin(usuarioID):
    listaID = lista_con_usuarioID(usuarioID)

    respuesta = requests.delete(f'{Ruta}/usuarios/{usuarioID}')
    lista = requests.delete(f'{Ruta}/listas/{listaID}')

    while lista.status_code != 404:
        listaID = lista_con_usuarioID(usuarioID)
        lista = requests.delete(f'{Ruta}/listas/{listaID}')

    return respuesta


def listaID_con_IDC(usuario,IDC): # Necesito devolver la listaID nada mas
    body = {'columna': 'usuario', 'buscar': usuario}
    respuesta = requests.get(f'{Ruta}/listas', json=body)  # USE UN GET PARA BUSCAR USUARIO

    if respuesta.status_code == 404:
        return respuesta

    listaID = respuesta.json()
    resultado = 0
    for value in listaID.values():
        if value['IDC'] == IDC:
            resultado = value['listaID']
            print(resultado)
    return resultado


def eliminar_lista_con_IDC_y_usuario(IDC,usuario):
    listaID = listaID_con_IDC(usuario, IDC)
    respuesta = requests.delete(f'{Ruta}/listas/{listaID}')
    return respuesta


def recomendados():  # Devuelve 3 comics ordenados de mayor a menor en un dict
    i = 0
    diccionario = {}
    ids = {}
    portadas = {}
    lista = []
    comics = buscar_comics('vistas', '*').json()
    while i < 3:
        diccionario[i] = comics[str(i)] # Guardo los 3 primeros comics con vistas en orden descendente
        ids[i] = "IDC"+str(diccionario[i]['IDC']) # Guardo los ID de las listas de arriba
        nombre = modelo_data.buscar_portadas(ids[i])
        portadas[i] = f'../static/img/portadas/{nombre}' # Aca guardo la ruta con el nombre
        i = i + 1 # aca sumo el contador... Porque explico boludeces?

    lista.append(diccionario)
    lista.append(portadas)
    lista.append(ids)
    # Arriba simplemente guarde los diccionarios en la lista que enviare, elegi lista en vez de dict porque me parece hasta mas sencilla de indezar, sin razon en realidad

    return lista # La lista envia los 3 comics en un dict, las 3 portadas en otro dict y las 3 id en OTRO dict

def agregar_lista_con_nombre(nombre):
    comics = lista_usuario(nombre) # le mando el nombre y me devuelve un json con las los comics en la lista de este usuario
    print(comics.content)

    try:
        if comics.status_code == 404:
            return "NOT FOUND", 404
        else:
            comics = comics.json()
        for value in comics.values():
            agregar_comic(value['URL'], nombre) # aca indeza entre los comics que recibi y le asigna al usuario esos comics
            print(value)
        return "OK", 200
    except Exception as e:
        print(e)
        return e

def indentificar_usuario(nombre):
    body_usuario = {'columna': 'nombre', 'buscar': nombre}
    respuesta_usuario = requests.get(f'{Ruta}/usuarios', json=body_usuario)  # USE UN GET PARA BUSCAR USUARIO

    if respuesta_usuario.status_code == 200:
        return "El usuario ya existe"
    else:
        return "OK", 200
