 function EnableDisableTextBox(btn) {
        var txtPassportNumber = document.getElementsByClassName("input");

        if (btn.value == "Cambiar") {
            for (var i = 0; i < 6; i++){
                 txtPassportNumber[i].removeAttribute("disabled");}
            btn.value = "Guardar";

        } else {
            for (var i = 0; i < 6; i++){
                txtPassportNumber[i].setAttribute("disabled", "disabled");}
            btn.value = "Cambiar";
        }
    }
function check(vari) {
if(vari == 1){
    document.getElementById("content").checked = true;
}else{
    document.getElementById("content").checked = false;}
}



function eliminar(){
const URL = 'http://127.0.0.1:5002/delete_user';
const xhr = new XMLHttpRequest();

if (confirm("¿Seguro que desea eliminar su cuenta?")) {
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
alert("Siempre hay segundas oportunidades!");
  return false
}
}


