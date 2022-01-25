from Comics.Datos.base_de_datos import BaseDeDatos


def login_usuario(nombre,email, contraseña):
    sql_usuario_login = f"""
    SELECT nombre FROM USUARIO
    WHERE nombre = '{nombre}' AND email = '{email}' AND contraseña = '{contraseña}'
    """

    bd = BaseDeDatos()
    lista = bd.ejecutar_sql(sql_usuario_login)

    if len(lista) == 1:
        return "OK", 200

    else:
        return "NOT FOUND", 404


def crear_usuario(nombre, contraseña,email, contenidoExplicito, rol):
    sql_tabla_usuarios = f"""
    INSERT INTO USUARIO(nombre, contraseña,email,contenidoExplicito, rol, fondo)
    VALUES ('{nombre}','{contraseña}','{email}','{contenidoExplicito}', '{rol}', '../img/animeScenary.jpg')
    """

    bd = BaseDeDatos()
    bd.ejecutar_sql(sql_tabla_usuarios)




def pedir_usuario(usuarioID):
    try:
        if type(usuarioID) == int:
            try:
                sql_pedir_usuario = f"""
                SELECT * FROM USUARIO 
                WHERE usuarioID = {usuarioID}
                """

                bd = BaseDeDatos()
                peticion = bd.ejecutar_sql(sql_pedir_usuario)
                peticion = peticion[0]

                base = ('usuarioID',
                        'nombre',
                        'contraseña',
                        'contenidoExplicito',
                        'rol')

                resultado = {}

                for index, value in enumerate(base):
                    resultado[value] = peticion[index]

                respuesta = "{\n" + "\n".join("{!r}: {!r},".format(k, v) for k, v in resultado.items()) + "\n}"

                return respuesta
            except:
                return "NOT FOUND", 404
        else:
            return "ERROR DE SINTAXIS", 412
    except:
        return "ERROR DE SINTAXIS", 412


def buscar_usuarios(columna, buscar):
    try:
        if columna == "*" and buscar =="*":
            sql_buscar_usuario = f"""
                        SELECT usuarioID, nombre,email, contenidoExplicito, rol
                        FROM USUARIO
                        """
        else:
            sql_buscar_usuario = f"""
            SELECT usuarioID, nombre,email, contenidoExplicito, rol
            FROM USUARIO 
            WHERE {columna} LIKE '{buscar}%' 
            ORDER BY UPPER({columna}) DESC
            """

        bd = BaseDeDatos()
        peticion = bd.ejecutar_sql(sql_buscar_usuario)

        base = ('usuarioID',
                'nombre',
                'email',
                'contenidoExplicito',
                'rol')

        lista_original = []
        respuesta = {}

        for i in peticion:
            for index, value in enumerate(base):
                respuesta[value] = i[index]
            lista_original.append(respuesta.copy())

            #POR ALGUNA RAZON SE REPITEN DICCIONARIOS DE LA ULTIMA
        diccionario = {}
        contador = 0

        for dict in lista_original:
            diccionario[contador] = dict
            contador = contador + 1

        try:
            'usuarioID' not in diccionario[0].keys()
        except:
            return "NOT FOUND", 404

        if len(diccionario) == 1:
            return diccionario[0]

        return diccionario

    except Exception as e:
        print("error en usuario",e)
        return e


def editar_usuario(usuarioID, nombre, email, contraseña, contenidoExplicito, rol):
    sql_detectar = f"""
    SELECT usuarioID FROM USUARIO
    WHERE usuarioID = {usuarioID}
    """

    bd = BaseDeDatos()
    prueba = bd.ejecutar_sql(sql_detectar)

    try:
        if usuarioID in prueba[0]:
            try:
                sql_editar_usuario = f"""
                UPDATE USUARIO SET nombre = '{nombre}',
                contraseña = '{contraseña}',
                contenidoExplicito = '{contenidoExplicito}',
                email = '{email}',
                rol = '{rol}'
                WHERE usuarioID = '{usuarioID}'
                """

                bd = BaseDeDatos()
                ejecucion = bd.ejecutar_sql(sql_editar_usuario)

                return "OK", 200

            except:
                return "ERROR DE SINTAXIS", 412
    except:
        return "NOT FOUND", 404

def eliminar_usuario(usuarioID):
    try:
        sql_detectar = f"""
        SELECT usuarioID FROM USUARIO
         WHERE usuarioID = {usuarioID}
        """

        bd = BaseDeDatos()
        respuesta = bd.ejecutar_sql(sql_detectar)
    except:
            return "NOT FOUND", 404

    if type(usuarioID) == int:
        if respuesta != []:
            try:
                sql_eliminar_usuario = f"""
                DELETE FROM USUARIO
                WHERE usuarioID='{usuarioID}'
                """
                bd = BaseDeDatos()
                bd.ejecutar_sql(sql_eliminar_usuario)

                return "OK", 200

            except:
                return 'NOT FOUND', 404
        else:
            return "NOT FOUND", 404
    else:
        return "El ID debe ser un NUMERO mayor a 0", 412


def cambiar_fondo(metodo,nombre, fondo):

    try:
        if metodo == 'GET':
            pedir_fondo = f"""
            SELECT fondo FROM USUARIO
            WHERE nombre = '{nombre}'
            """

            bd = BaseDeDatos()
            respuesta = bd.ejecutar_sql(pedir_fondo)[0][0]
            return respuesta

        if metodo == 'UPDATE':
            cambiar_fondo = f"""
                            UPDATE USUARIO SET fondo = {fondo}
                            WHERE nombre = '{nombre}'
                            """

            bd = BaseDeDatos()
            bd.ejecutar_sql(cambiar_fondo)
            return "OK", 200

    except Exception as e:
        print(e)
        return e