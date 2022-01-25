function mostrar() {
    document.getElementById("sidebar").style.width = "300px";
    document.getElementById("contenido").style.marginLeft = "300px";
    document.getElementById("menu").style.display = "none";
    document.getElementById("menu").className = "abierto";

}

function ocultar() {
    document.getElementById("sidebar").style.width = "0";
    document.getElementById("contenido").style.marginLeft = "0";
    document.getElementById("menu").style.display = "inline";
    document.getElementById("menu").className = "cerrado";

}

function cambiar()
{
    var elem = document.getElementById("menu");
    if (elem.className=="cerrado") mostrar();
    else ocultar();
}
var fondos = ["../static/img/8b147f90e02a61d267600245b4541f64.jpg","../static/img/descarga1.jpg","../static/img/descarga2.jpg","../static/img/animeScenary.jpg"]

function cambiar_fondo(variable) {
var image = fondos[variable];
document.body.style.backgroundImage = "url(" + image + ")";

const URL = 'http://127.0.0.1:5002/fondo'
const xhr = new XMLHttpRequest();
sender = JSON.stringify(image)
xhr.open('POST', URL);
xhr.send(sender);
}



