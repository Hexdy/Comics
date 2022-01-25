function reqListener () {
  console.log(this.responseText);
}


function compartir(codigo){
const URL = 'http://127.0.0.1:5002/compartir';
const xhr = new XMLHttpRequest();



if(codigo == 404){
xhr.responseType = 'text';

xhr.open('GET', URL, true);
xhr.send();
xhr.addEventListener("load", reqListener);


xhr.onreadystatechange = function (aEvt) {
  if (xhr.readyState == 4) {
     if(xhr.status == 200){
        var text = xhr.responseText;
        const elem = document.createElement('textarea');
        elem.value = text;
        document.body.appendChild(elem);
        elem.select();
        document.execCommand('copy');
        document.body.removeChild(elem);
        }
    }
  }
}else{

xhr.open('POST', URL);
xhr.send(codigo);
}
}

PERO PORQUE NO PUEDO CREAR ALGO ASI AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA