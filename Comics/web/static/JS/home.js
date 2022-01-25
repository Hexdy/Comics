function eliminar_lista(IDC){
const URL = 'http://127.0.0.1:5002/delete_list_user';
const xhr = new XMLHttpRequest();

sender = JSON.stringify(IDC);
xhr.open('POST', URL);
xhr.send(sender);
var cosa = ""+IDC+"";
var variable = document.getElementById('IDC'+IDC+'');

if (variable){
variable.remove();
}else{
document.getElementById('IDCB'+IDC+'').remove();
}
}


