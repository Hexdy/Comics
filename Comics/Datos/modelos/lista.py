from Comics.Datos.base_de_datos import BaseDeDatos


def modificar_nombre_lista(usuarioID, nombre):
    try:
        sql_editar_lista = f"""
                    UPDATE LISTA SET 
                    usuario='{nombre}'
                    WHERE usuarioID = '{usuarioID}'
                    """
        bd = BaseDeDatos()
        bd.ejecutar_sql(sql_editar_lista)

        return "OK", 200
    except Exception as e:
        return e


def crear_lista(usuarioID, IDC):
    bd = BaseDeDatos()
    sql_contingencia = f"""
                SELECT listaID FROM LISTA WHERE IDC ='{IDC}' AND usuarioID = '{usuarioID}'
                """
    contingencia = bd.ejecutar_sql(sql_contingencia)

    if len(contingencia) == 1:
        return "ERROR DE CONTINGENCIA", 409

    sql_nombre = f"""
            SELECT nombre FROM COMIC WHERE IDC='{IDC}'
            """
    sql_usuario = f"""
        SELECT nombre FROM USUARIO WHERE usuarioID='{usuarioID}'
        """

    sql_idc = f"""
        SELECT IDC FROM COMIC WHERE IDC='{IDC}'
        """

    sql_usuarioID = f"""
            SELECT usuarioID FROM USUARIO WHERE usuarioID='{usuarioID}'
            """

    usuarioID = bd.ejecutar_sql(sql_usuarioID)
    usuario = bd.ejecutar_sql(sql_usuario)
    nombre = bd.ejecutar_sql(sql_nombre)
    idc = bd.ejecutar_sql(sql_idc)

    if idc:
        if usuarioID:
            sql_usuario_en_comic = f"""
                INSERT INTO LISTA(usuarioID, usuario, IDC, nombreComic) VALUES('{usuarioID[0][0]}','{usuario[0][0]}','{idc[0][0]}', '{nombre[0][0]}')
                """

            bd.ejecutar_sql(sql_usuario_en_comic)
            return "OK", 200
        else:
            return "ID DE USUARIO NO ENCONTRADO", 404
    else:
        return "IDC NO ENCONTRADO", 404


def pedir_lista(listaID):
    try:
        if type(listaID) == int:
            try:
                sql_pedir_lista = f"""
                SELECT * FROM LISTA 
                WHERE listaID = {listaID}
                """

                bd = BaseDeDatos()
                peticion = bd.ejecutar_sql(sql_pedir_lista)
                peticion = peticion[0]

                base = ('listaID',
                        'usuario',
                        'IDC',
                        'nombreComic')

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


def buscar_lista(columna, buscar):
    try:
        if buscar == '*':
            sql_buscar_usuario = f"""
                        SELECT *
                        FROM LISTA
                        """
        else:
            if columna == 'URL':
                sql_buscar_usuario = f"""
                            SELECT listaID,usuarioID,usuario, IDC, nombreComic
                            FROM LISTA 
                            WHERE {columna} = '{buscar}%'
                            """
            else:
                sql_buscar_usuario = f"""
                            SELECT listaID,usuarioID,usuario, IDC, nombreComic
                            FROM LISTA 
                            WHERE {columna} = '{buscar}' 
                            ORDER BY UPPER({columna}) DESC
                            """
        bd = BaseDeDatos()
        peticion = bd.ejecutar_sql(sql_buscar_usuario)

        base = ('listaID',
                'usuarioID',
                'usuario',
                'IDC',
                'nombreComic')

        lista_original = []

        for i in peticion:
            result = {}
            for index, value in enumerate(base):
                result[value] = i[index]
            lista_original.append(result)

        diccionario = {}
        contador = 0

        for dict in lista_original:
            diccionario[contador] = dict
            contador = contador + 1

        try:
            'listaID' not in diccionario[0].keys()
        except:
            return "NOT FOUND", 404

        return diccionario

    except:
        return "ERROR DE SINTAXIS", 412


def editar_lista(listaID, usuarioID, IDC):
    try:
        sql_detectar = f"""
        SELECT listaID FROM LISTA
        WHERE listaID = '{listaID}'
        """
        sql_detectar_2 = f"""
        SELECT usuarioID FROM USUARIO
        WHERE usuarioID = '{usuarioID}'
        """
        sql_detectar_3 = f"""
            SELECT IDC FROM COMIC
            WHERE IDC = '{IDC}'
            """

        bd = BaseDeDatos()
        prueba2 = bd.ejecutar_sql(sql_detectar_2)
        prueba3 = bd.ejecutar_sql(sql_detectar_3)
        prueba = bd.ejecutar_sql(sql_detectar)
        if not prueba:
            return "ID de la lista no encontrado", 404
        if not prueba2:
            return "Usuario no encontrado", 404
        if not prueba3:
            return "ID del comic no encontrado", 404

        sql_conseguir_nombre_comic = f"""
            SELECT nombre FROM COMIC WHERE IDC = {IDC}
            """

        nombre_1 = bd.ejecutar_sql(sql_conseguir_nombre_comic)
        nombre = nombre_1[0][0]

        sql_conseguir_usuario = f"""
                SELECT nombre FROM USUARIO WHERE usuarioID = '{usuarioID}'
                """

        usuario_1 = bd.ejecutar_sql(sql_conseguir_usuario)
        usuario = usuario_1[0][0]

        if prueba:
            try:
                sql_editar_lista = f"""
                    UPDATE LISTA SET 
                    IDC = '{IDC}',
                    usuarioID = '{usuarioID}',
                    usuario='{usuario}',
                    nombreComic = '{nombre}'
                    WHERE listaID = {listaID}
                    """

                bd.ejecutar_sql(sql_editar_lista)

                return "OK", 200
            except:
                return "ERROR DE SINTAXIS", 412
        else:
            return "ERROR DE SINTAXIS", 412
    except:
        return "NOT FOUND", 404


def eliminar_lista(listaID):
    try:
        sql_detectar = f"""
            SELECT listaID FROM LISTA
            WHERE listaID = {listaID}
            """

        bd = BaseDeDatos()
        respuesta = bd.ejecutar_sql(sql_detectar)

    except:
        return "NOT FOUND", 404

    if type(listaID) == int:
        if respuesta != []:
            try:
                sql_eliminar_lista = f"""
                        DELETE FROM LISTA
                        WHERE listaID='{listaID}'
                        """

                bd = BaseDeDatos()
                bd.ejecutar_sql(sql_eliminar_lista)

                return "OK", 200

            except:
                return 'NOT FOUND', 404
        else:
            return "NOT FOUND", 404
    else:
        return "ERROR DE SINTAXIS", 412
