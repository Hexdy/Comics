from os import listdir
from os.path import isfile, join
import re

def buscar_portadas(nombre):
    archivos = [f for f in listdir("E:\pythonProject2\Comics\web\static\img\portadas") if
                isfile(join("E:\pythonProject2\Comics\web\static\img\portadas", f))]

    respuesta = [x for x in archivos if re.match(f"{nombre}", x)]
    return respuesta[0]  # Devolvera un string



"""
id = 'casita'
texto = 'data 4'
# ARRIBA DI LOS DATOS QUE USARE NORMALMENTE, EL ID (YA SEA DE USUARIO O COMIC) Y EL TEXTO (YA SEA EL REPORT O LA SINOPSIS)


hoe = open(f'E:\pythonProject2\Comics\web\static\data\{id}.txt').read()


with open(f'E:\pythonProject2\Comics\web\static\data\{id}.txt', 'w') as f:
    f.write(hoe + '\n'+f'%%->{texto}<')  # aca hace que se sumen, los items se suman correctamente (FIFO) aunque queda un renglon vacio al inicio
    f.close()  # ACA LO CIERRO, POR FORRO


# ACA BUSCO LA INFO CON EL ID CORRESPONDIENTE (SERIA BUENO DARLES UN ID A CADA PARTE)
hoe = open(f'E:\pythonProject2\Comics\web\static\data\{id}.txt').read()
open(f'E:\pythonProject2\Comics\web\static\data\{id}.txt').close()


pattern = "%%->(.*?)<"
substring = re.findall(pattern, hoe)
"""
