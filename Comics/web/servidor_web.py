# Maximiliano da silva, grupo 18: comics, Servidor Web V0.1
from datetime import timedelta
from flask import Flask, request, render_template, url_for, session
from werkzeug.utils import redirect
from servicios import autenticacion_web

app = Flask(__name__)
app.secret_key = "12312ok3o1i23oi12n3oi12n3oi12n3in12o3in1 ipjpoj12i90c3j1028c3 1802uj3c128"
app.permanent_session_lifetime = timedelta(hours=1)


# ////////////////////////////////////////////////////////SERVIDOR//////////////////////////////////////////////////////
# LOGIN/INDEX
@app.route('/', methods=['GET', 'POST'])
def login():
    if 'usuario' in session:
        return redirect(url_for('home'))

    if request.method == 'POST':

        if not autenticacion_web.login(request.form['name'], request.form['email'], request.form['password']):
            session['error'] = 'Credenciales inválidas'
        else:
            session.permanent = True
            if 'fondo' not in session:
                session['fondo'] = str(autenticacion_web.fondo('GET', request.form['name'], '').content, 'utf-8')

            session['usuario'] = request.form['name']
            session['email'] = request.form['email']
            session['contraseña'] = request.form['password']
            rol = autenticacion_web.buscar_usuario('nombre', session['usuario']).json()
            session['rol'] = rol['rol']
            session['contenidoExplicito'] = autenticacion_web.contenido_explicito(session['usuario'])
            return redirect(url_for('home'))

    if 'error' in session:
        error = session['error']
        session['error'] = None
    else:
        error = None

    return render_template('login.html', error=error)


# SIGNUP ///////////////NO ACEPTABLEMENTE COMPLETO
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if 'usuario' in session:
        return redirect(url_for('home'))

    if request.method == 'POST':
        if request.form['name'] == '*':
            session['error'] = 'Necesitas un nombre valido'
            return redirect(url_for('signup'))
        else:
            if not request.form['confirm'] == request.form['passwd']:
                session['error'] = 'La contraseña no coincide'
                return redirect(url_for('signup'))
            else:
                if type(autenticacion_web.indentificar_usuario(request.form['name'])) == str:
                    session['error'] = autenticacion_web.indentificar_usuario(request.form['name'])
                    return redirect(url_for('signup'))

                if not autenticacion_web.signup(request.form['name'], request.form['email'], request.form['passwd']):
                    session['error'] = 'Credenciales inválidas'
                    return redirect(url_for('signup'))
                else:
                    autenticacion_web.login(request.form['name'], request.form['email'], request.form['passwd'])
                    session.permanent = True


                    session['usuario'] = request.form['name']
                    session['email'] = request.form['email']
                    session['contraseña'] = request.form['passwd']
                    session['fondo'] = "../static/img/animeScenary.jpg"
                    session['rol'] = "Administrador"
                    session['contenidoExplicito'] = autenticacion_web.contenido_explicito(session['usuario'])
                    return redirect(url_for('home'))

    if 'error' in session:
        error = session['error']
        session['error'] = None
    else:
        error = None

    return render_template('signup.html', error=error)


# HOME
@app.route('/home', methods=['GET', 'POST'])
def home():
    error = ""
    if not 'usuario' in session:
        return redirect(url_for('login'))

    usuario = session['usuario']
    lista = autenticacion_web.lista_usuario(usuario)

    try:
        if lista.status_code == 404:
            lista = None

    except:
        session['lista'] = lista
        if 'error' in session:
            error = session['error']
            session['error'] = None
        else:
            error = None

    # antes que nada necesito pedir los comics con mas vistas y usar sus ID para indezar en la portada y sinopsis
    data = autenticacion_web.recomendados()

    sino1 = open(f"E:\pythonProject2\Comics\web\static\data\sinopsis\{data[2][0]}.txt").read()
    open(f"E:\pythonProject2\Comics\web\static\data\sinopsis\{data[2][0]}.txt").close()

    sino2 = open(f"E:\pythonProject2\Comics\web\static\data\sinopsis\{data[2][1]}.txt").read()
    open(f"E:\pythonProject2\Comics\web\static\data\sinopsis\{data[2][1]}.txt").close()

    sino3 = open(f"E:\pythonProject2\Comics\web\static\data\sinopsis\{data[2][2]}.txt").read()
    open(f"E:\pythonProject2\Comics\web\static\data\sinopsis\{data[2][2]}.txt").close()

    # los datos que recibe son autor, genero, rating, vistas, capitulos e idioma, ademas de la direccion de la portada
    return render_template('home.html',
                           usuario=usuario,
                           lista=lista,
                           error=error,
                           fondo=session['fondo'],
                           rol=session['rol'],
                           data_recom=data[0],  # Aca se envian los comics como un dict
                           port1=data[1][0], port2=data[1][1], port3=data[1][2],
                           # aca envio las portadas como rutas al archivo
                           sino1=sino1, sino2=sino2, sino3=sino3,  # aca se envian las sinopsis como strings enormes
                           contenido=session['contenidoExplicito']
                           )


@app.route('/account', methods=['GET', 'POST'])
def account():
    if not 'usuario' in session:
        return redirect(url_for('login'))

    passwd = "*" * len(session['contraseña'])
    confirm = passwd
    if 'error' in session:
        error = session['error']
        session['error'] = None
    else:
        error = None
    return render_template('modificar_cuenta.html', name=session['usuario'], confirm=confirm, passwd=passwd,
                           email=session['email'], error=error, contenido=session['contenidoExplicito'],
                           fondo=session['fondo'])


@app.route('/admin', methods=['GET', 'POST', 'DELETE', 'UPDATE'])
def admin():
    try:
        if not 'usuario' in session:
            return redirect(url_for('login'))

        if session['rol'] != 'Administrador':
            return redirect(url_for('home'))

        if not 'busqueda_comic' in session:
            session['busqueda_comic'] = autenticacion_web.buscar_comics('*', '*').json()
            comics = session['busqueda_comic']
            session.pop('busqueda_comic', None)
            # si detecta que no hay un ingreso externo en comics busca todos los comics
        else:
            comics = session['busqueda_comic']
            session.pop('busqueda_comic', None)

        if 'busqueda' not in session:
            session['busqueda'] = autenticacion_web.buscar_usuario('*', '*').json()

            users = session['busqueda']
            lista = None
            session.pop('busqueda', None)
            session.pop('busqueda_lista', None)

            # Aqui verifica si hay ya datos en session, sino busca todos
        else:
            users = session['busqueda']
            lista = session['busqueda_lista']
            session.pop('busqueda', None)
            session.pop('busqueda_lista', None)

        if 'error' in session:
            error = session['error']
            session['error'] = None
        else:
            error = None

        return render_template('lista_usuario.html', users=users, lista=lista, comics=comics, error=error,
                               idu=autenticacion_web.usuarioID_con_nombre(session['usuario']))
    except Exception as e:
        print(e)
        return e


# NO NECESARIO O UTIL ACTUALMENTE
"""@app.route('/report', methods=['GET', 'POST'])
def report():
    if not 'usuario' in session:
        return redirect(url_for('login'))
    if 'error' in session:
        error = session['error']
        session['error'] = None
    else:
        error = None

    return render_template('report.html', error=error, fondo=session['fondo'])"""


# --------------------------------------------------------ACCIONES------------------------------------------------------
@app.route('/process_url', methods=['POST', 'GET'])
def process_url():
    if not 'usuario' in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        url = request.form['URL']
        if len(url) < 3 or len(url) > 63:
            session['error'] = "La url es incorrecta, intente otra vez"
            return redirect(url_for('home'))

        usuario = session['usuario']
        autenticacion = autenticacion_web.agregar_comic(url, usuario)

        if autenticacion.status_code == 200:
            return redirect(url_for('home'))

        if autenticacion.status_code == 404:
            session['error'] = autenticacion.text
            return redirect(url_for('home'))

        if autenticacion.status_code == 409:
            session['error'] = autenticacion.text
            return redirect(url_for('home'))

        if autenticacion == str:
            session[
                'error'] = autenticacion  # Estaria bueno un javascript que muestre este mensaje debajo de la casilla URL
        else:
            lista = autenticacion_web.lista_usuario(usuario)
            session['lista'] = lista
            return redirect(url_for('home'))


@app.route('/mod_user', methods=['POST', 'GET', 'PUT'])
def mod_user():
    if not 'usuario' in session:
        return redirect(url_for('login'))

    d = {'name': '', 'password': '', 'confirm': '', 'email': '', 'content': ''}
    fields = ['name', 'password', 'confirm', 'email', 'content']

    if request.method == 'POST':

        for field in fields:
            d[field] = request.form.get(field, None)

        if d['content'] == 'result':
            session['contenidoExplicito'] = 1
            d['content'] = 1
        else:
            session['contenidoExplicito'] = 0
            d['content'] = 0

        if d['confirm'] != d['password']:  # Detecta si la confirmacion de la contraseña y la contraseña son iguales
            session['error'] = "La contraseña y la confirmacion han de ser iguales."
            return redirect(url_for('account'))

        del d['confirm']

        if not d['name']:
            d['name'] = session['usuario']
        else:
            autenticacion = autenticacion_web.confirmar_nombre(d['name'])
            if autenticacion[1] == 409:
                session['error'] = "Ese nombre ya existe"
                return redirect(url_for('account'))

        if not d['password']:
            d['password'] = session['contraseña']

        if not d['email']:
            d['email'] = session['email']

        autenticacion_web.modificar_usuario(session['usuario'], d['name'], d['email'], d['password'],
                                            d['content'])

        session['usuario'] = d['name']
        session['contraseña'] = d['password']
        session['email'] = d['email']

    return redirect(url_for('account'))


@app.route('/logout')
def logout():
    if not 'usuario' in session:
        return redirect(url_for('login'))

    for key in list(session.keys()):
        session.pop(key)
    return redirect(url_for('login'))


@app.route('/delete_user', methods=['POST', 'GET', 'DELETE'])
def delete():
    if not 'usuario' in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        nombre = session['usuario']
        respuesta = autenticacion_web.eliminar_usuario(nombre)

        if type(respuesta) != str:
            session['error'] = "El usuario no pudo ser eliminado"
            return redirect(url_for('account'))
        else:
            for key in list(session.keys()):
                session.pop(key)
            return redirect(url_for('login'))


@app.route('/busqueda', methods=['POST', 'GET'])
def busqueda():
    if not 'usuario' in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        if request.form['seleccion'] == 'nombre':

            if autenticacion_web.buscar_usuario(request.form['seleccion'], request.form['buscar']).status_code == 200:
                session['busqueda'] = autenticacion_web.buscar_usuario(request.form['seleccion'],
                                                                       request.form['buscar']).json()

            else:
                session['busqueda'] = None

        if request.form['seleccion'] != 'nombre':
            resultado = autenticacion_web.buscar_usuario(request.form['seleccion'], request.form['buscar'])

            if resultado.status_code == 404:
                session['busqueda_lista'] = None
                session['busqueda'] = None
            else:
                session['busqueda'] = autenticacion_web.buscar_usuario(request.form['seleccion'],
                                                                       request.form['buscar']).json()
                respuesta = autenticacion_web.lista_alterna(resultado.json())
                session['busqueda_lista'] = respuesta

        if not type(autenticacion_web.lista_usuario(request.form['buscar'])) == dict:
            session['busqueda_lista'] = None
            # este es el caso en que la lista venga con error/vacia
        else:
            session['busqueda_lista'] = autenticacion_web.lista_usuario(request.form['buscar'])

    return redirect(url_for('admin'))


@app.route('/busqueda_comic', methods=['POST', 'GET'])
def busqueda_comics():
    if not 'usuario' in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        data = autenticacion_web.buscar_comics(request.form['seleccion_comic'], request.form['buscar_comic'])

        if data.status_code == 200:
            session['busqueda_comic'] = data.json()
        else:
            if data.status_code == 404:
                session['busqueda_comic'] = None
                session['error'] = "Comic no encontrado."
            else:
                session['error'] = "ha"
                session['busqueda_comic'] = None

        return redirect(url_for('admin'))


@app.route('/fondo', methods=['PUT', 'POST'])
def cambiar_fondo():
    if not 'usuario' in session:
        return redirect(url_for('login'))

    data = str(request.data, 'utf-8')
    session['fondo'] = data
    autenticacion_web.fondo('UPDATE', session['usuario'], data)
    return "ok", 200


@app.route('/agregar_comic', methods=['POST'])
def agregar_comic():
    if not 'usuario' in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        data = {
            'nombre': request.form['nombre_comic'],
            'genero': request.form['genero_comic'],
            'autor': request.form['autor_comic'],
            'idioma': request.form['idioma_comic'],
            'ultimaEmision': request.form['ultima_emision_comic'],
            'ultimoCapitulo': request.form['ultimo_capitulo_comic'],
            'estado': request.form['estado_comic'],
            'pagina': request.form['pagina_comic'],
            'rating': request.form['rating_comic'],
            'URL': request.form['URL_comic']
        }
        resource = autenticacion_web.crear_comic(data)

        if type(resource) == tuple:
            session['error'] = resource[0]

        return redirect(url_for('admin'))


@app.route('/delete_comic_admin', methods=['POST', 'GET', 'DELETE'])
def delete_comic_admin():
    if not 'usuario' in session:
        return redirect(url_for('login'))

    value = int(request.data)
    autenticacion_web.eliminar_comic_simple(value)
    return redirect(url_for('admin'))


@app.route('/delete_user_admin', methods=['POST', 'GET', 'DELETE'])
def delete_user_admin():
    if not 'usuario' in session:
        return redirect(url_for('login'))

    data = int(request.data)  # recibe el usuarioID, un integer

    autenticacion_web.eliminar_usuario_admin(data)

    return redirect(url_for('admin'))


@app.route('/delete_list_user', methods=['POST', 'GET', 'DELETE'])
def delete_list_user():
    if not 'usuario' in session:
        return redirect(url_for('login'))

    value = int(request.data)
    autenticacion_web.eliminar_lista_con_IDC_y_usuario(value, session['usuario'])
    return redirect(url_for('admin'))







# --------EJECUCIÓN----------
if __name__ == '__main__':
    app.debug = True
    app.run(port=5002, host='0.0.0.0')
