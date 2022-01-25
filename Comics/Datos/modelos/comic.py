from Comics.Datos.base_de_datos import BaseDeDatos


def crear_comic(nombre, genero, autor, idioma, ultimaEmision, ultimoCapitulo, estado, pagina, rating, URL):
    # hay 10 valores para los comics, ya que exceptúo el usuarioID que se agrega aparte y el IDC que es autogenerado
    bd = BaseDeDatos()
    determinar_error_sql = f"""SELECT URL from COMIC WHERE URL = '{URL}'
                            """
    resultado_prueba = bd.ejecutar_sql(determinar_error_sql)
    if resultado_prueba:
        return "ERROR DE CONTINGENCIA", 409
    sql_tabla_comics = f"""
        INSERT INTO COMIC(nombre, genero, autor, idioma, ultimaEmision, ultimoCapitulo, estado, pagina, rating, URL)
        VALUES (
        '{nombre}',
        '{genero}',
        '{autor}',
        '{idioma}',
        '{ultimaEmision}',
        '{ultimoCapitulo}',
        '{estado}',
        '{pagina}',
        '{rating}',
        '{URL}'
        )
    """
    # La URL ha de ser unica incluso en las pruebas
    bd.ejecutar_sql(sql_tabla_comics)
    if nombre or genero or autor or idioma or ultimaEmision or ultimoCapitulo or estado or pagina or rating or URL == '*':
        return "ERROR DE CONTINGENCIA", 409
    return "OK", 200


def pedir_comic(IDC):
    try:
        if type(IDC) == int:
            try:
                sql_pedir_comic = f"""
                SELECT * FROM COMIC 
                WHERE IDC = '{IDC}'
                """

                bd = BaseDeDatos()
                peticion = bd.ejecutar_sql(sql_pedir_comic)

                peticion = peticion[0]

                base = ('IDC',
                        'nombre',
                        'genero',
                        'autor',
                        'idioma',
                        'estado',
                        'ultimaEmision',
                        'ultimoCapitulo',
                        'pagina',
                        'rating',
                        'URL',
                        'vistas',
                        'explicito')
                resultado = {}

                for index, value in enumerate(base):
                    resultado[value] = peticion[index]



                return resultado
            except:
                return "NOT FOUND", 404
        else:
            return "ERROR DE SINTAXIS", 412
    except:
        return "ERROR DE SINTAXIS", 412


def buscar_comic(columna, buscar):
    try:
        if buscar == '*':
            if columna == 'vistas':
                sql_buscar_comic = f"""SELECT * FROM COMIC ORDER BY vistas DESC
                                        """

            else:
                sql_buscar_comic = f"""
                        SELECT * FROM COMIC
                        """

        else:
            if columna == 'URL':
                sql_buscar_comic = f"""
                                    SELECT *
                                    FROM COMIC 
                                    WHERE URL = '{buscar}'
                                    """
            else:
                sql_buscar_comic = f"""
                                    SELECT *
                                    FROM COMIC 
                                    WHERE {columna} LIKE '{buscar}%' 
                                    ORDER BY UPPER({columna}) ASC
                                    """

        bd = BaseDeDatos()
        peticion = bd.ejecutar_sql(sql_buscar_comic)

        base = ('IDC',
                'nombre',
                'genero',
                'autor',
                'idioma',
                'estado',
                'ultimaEmision',
                'ultimoCapitulo',
                'pagina',
                'rating',
                'URL',
                'vistas',
                'explicito')

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
            if 'IDC' in diccionario[0].keys():
                return diccionario
        except:
            return "NOT FOUND", 404
    except Exception as e:
        return e

def editar_comic(IDC, nombre, genero, autor, idioma, estado,
                 ultimaEmision, ultimoCapitulo, pagina, rating):
    sql_detectar = f"""
    SELECT IDC FROM COMIC
    WHERE IDC = '{IDC}'
    """

    bd = BaseDeDatos()
    prueba = bd.ejecutar_sql(sql_detectar)

    try:
        if IDC in prueba[0]:
            try:
                sql_editar_comic = f"""
                    UPDATE COMIC SET
                    nombre='{nombre}',
                    genero='{genero}',
                    autor='{autor}',
                    idioma='{idioma}',
                    estado='{estado}',
                    ultimaEmision='{ultimaEmision}',
                    ultimoCapitulo='{ultimoCapitulo}',
                    pagina='{pagina}',
                    rating='{rating}'
                    WHERE IDC = {IDC}
                    """

                bd = BaseDeDatos()
                bd.ejecutar_sql(sql_editar_comic)

                return "OK", 200

            except:
                return "ERROR DE SINTAXIS", 412
    except:
        return "NOT FOUND", 404


def agregar_vistas(IDC):
    sql_vistas_actuales = f"""
        SELECT vistas FROM COMIC
        WHERE IDC = '{IDC}'
        """

    bd = BaseDeDatos()
    vista = bd.ejecutar_sql(sql_vistas_actuales)
    vistas = vista[0][0] + 1

    try:
        sql_editar_comic = f"""
                    UPDATE COMIC SET
                    vistas='{vistas}'
                    WHERE IDC = {IDC}
                    """

        bd = BaseDeDatos()
        bd.ejecutar_sql(sql_editar_comic)

        return "OK", 200

    except Exception as e:
        return e


def eliminar_comic(IDC):
    try:
        sql_detectar = f"""
        SELECT IDC FROM COMIC
        WHERE IDC = '{IDC}'
        """
        bd = BaseDeDatos()
        respuesta = bd.ejecutar_sql(sql_detectar)
    except:
        return "NOT FOUND", 404

    if type(IDC) == int:
        if respuesta != []:
            try:
                sql_eliminar_comic = f"""
                    DELETE FROM COMIC
                    WHERE IDC={IDC}
                    """
                bd = BaseDeDatos()
                bd.ejecutar_sql(sql_eliminar_comic)

                return "OK", 200

            except:
                return 'NOT FOUND', 404
        else:
            return "NOT FOUND", 404
    else:
        return "El IDC debe ser un NUMERO mayor a 0", 412
