function copiar(a) {
text = a.innerHTML
const elem = document.createElement('textarea');
elem.value = text;
document.body.appendChild(elem);
elem.select();
document.execCommand('copy');
document.body.removeChild(elem);
}

function buscar(variable, variable2){
var text = variable.value;

}
function tittle(){
 for (var i = 0; i < document.getElementsByTagName("a").length; i++){
         document.getElementsByTagName("a")[i].title = document.getElementsByTagName("a")[i].innerHTML;
        }

}

function eliminar_comic(IDC){
const URL = 'http://127.0.0.1:5002/delete_comic_admin';
const xhr = new XMLHttpRequest();
if (confirm("¿Seguro que desea eliminar este comic?")) {
sender = JSON.stringify(IDC);
xhr.open('POST', URL);
xhr.send(sender);
document.getElementById('comic'+IDC+'').remove();
} else {
  return false
}
}

function eliminar_usuario(usuarioID, propiaID){
var idu = propiaID;
const xhr = new XMLHttpRequest();
if(usuarioID==idu){
if (confirm("¿Seguro que desea eliminar su cuenta?")) {

const URL = 'http://127.0.0.1:5002/delete_user';
sender = JSON.stringify();
xhr.open('POST', URL);
xhr.send(sender);
xhr.onreadystatechange = function (aEvt) {
  if (xhr.readyState == 4) {
     if(xhr.status == 200){
location.reload();

        }
    }
  }
} else {

  return false

}
}else{

const URL = 'http://127.0.0.1:5002/delete_user_admin';
if (confirm("¿Seguro que desea eliminar este usuario?")) {
sender = JSON.stringify(usuarioID);
xhr.open('POST', URL);
xhr.send(sender);
document.getElementById('user'+usuarioID+'').remove();

} else {
  return false
}
}}

