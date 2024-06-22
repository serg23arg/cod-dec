from random import randint, shuffle, choices
from math import ceil
from os import system

# FUNCIONES PARA CODIFICAR:

# Tomando como base una lista de todos los caracteres codificables, se genera una nueva lista randomizada.
def randomizar_abc_lista(abc_tupla): 
    
    abc_lista = list(abc_tupla)
    abc_lista_modificada = []
    clave = ''
    total_i_abc = len(abc_tupla)-1

    for i in range (len(abc_tupla)):

        if total_i_abc > 0:
            i_random = randint(0,total_i_abc)
            abc_lista_modificada.append(abc_lista.pop(i_random))               
            total_i_abc -= 1
            clave += f'{i_random:02}'
        else:
            abc_lista_modificada.append(abc_lista.pop())
            clave = clave + '00'
            
    return abc_lista_modificada, clave


# Con la lista randomizada (modificada) se genera un diccionario y una clave de cifrado para el mismo.
def generar_diccionario(abc_lista_modificada):

    diccionario = {}
    codigo = 1

    for c in abc_lista_modificada:
                
        valor = f'{codigo:02}'
        diccionario[c] = valor
        codigo += 1            
    
    return diccionario


# Una vez construidos los 5 diccionarios necesarios, se pide al usuario ingresar el mensaje a codificar, y el mismo es cifrado utilizando los 5 diccionarios anteriormente creados, de forma rotativa continua hasta el fin del mensaje.
def codificar_mensaje(diccionario1, diccionario2, diccionario3, diccionario4, diccionario5, abc_tupla):

    mensaje_original = input('Enter message: ')
    mensaje_codificado = ''
    diccionarios = (diccionario1, diccionario2, diccionario3, diccionario4, diccionario5)
    rotador = 0

    for c in mensaje_original:
        
        if c in abc_tupla:
            mensaje_codificado += diccionarios[rotador][c]         
        else:
            mensaje_codificado += c
        
        rotador = (rotador + 1) % len(diccionarios)
    
    return mensaje_codificado


# Al mensaje codificado se le incorporan las claves, también de forma codificada, y así como la "clave de claves".
# Como última capa de seguridad, se agregan caracteres aleatorios al mensaje, a fin de hacerlo más confuso.
# Luego se exporta el mensaje en formato txt para su posterior envio por otro medio.
def exportar(clave1, clave2, clave3, clave4, clave5, mensaje_codificado, mascara):

    lista_claves = (clave1, clave2, clave3 ,clave4 ,clave5)
 
    posiciones_base = [0, 1, 2, 3, 4]
    shuffle(posiciones_base)
    orden_claves = ''.join(map(str, posiciones_base))
    
    for i in posiciones_base:
        mensaje_codificado = lista_claves[i][:87] + mensaje_codificado + lista_claves[i][87:]

    mensaje_codificado = orden_claves + mensaje_codificado

    seleccion_c = choices(mascara, k=ceil(len(mensaje_codificado)*0.20))
    posiciones = choices(range(1, len(mensaje_codificado)-1), k=len(seleccion_c))
    indice_p = 0
    mensaje_enmascarado = mensaje_codificado

    for e in seleccion_c:
        mensaje_enmascarado = mensaje_enmascarado[:posiciones[indice_p]] + e + mensaje_enmascarado[posiciones[indice_p]:]
        indice_p += 1
    
    nombre = input('Input desired filename to save:')
    nombretxt = f'{nombre}.txt'
    with open(nombretxt, "w") as archivo:
         archivo.write(mensaje_enmascarado)

# FUNCIONES PARA DECODIFICAR:

# Se importa el mensaje codificado en formato txt, removiéndo en el proceso los carácteres agregados al final de la codificación.
def importar(mascara):

    archivo = input('Input filename to decode (without extension):')
    ruta = f'./{archivo}.txt'

    try:
        with open(ruta, "r") as archivo:
            mensaje_enmascarado = archivo.read()
    except FileNotFoundError:
        print('File not found.')
        return importar()
    
    mensaje_codificado = ''.join([c for c in mensaje_enmascarado if c not in mascara])

    return mensaje_codificado


# Se recomponen las claves utilizando para ello la "clave de claves" incorporada al mensaje codificado, y se eliminan todos los caracteres que no pertenezcan al mensaje en sí.
def recuperar_claves(mensaje_codificado):
    
    orden_claves = mensaje_codificado[:5][::-1]
    mensaje_codificado = mensaje_codificado [5:]

    lista_claves_1 = [0,0,0,0,0]
    lista_claves_2 = [0,0,0,0,0]

    for i in orden_claves:
        i = int(i)
        lista_claves_1[i] = mensaje_codificado[:87]
        lista_claves_2[i] = mensaje_codificado[-87:]
        mensaje_codificado = mensaje_codificado[87:-87]
    
    clave1 = lista_claves_1[0] + lista_claves_2[0]
    clave2 = lista_claves_1[1] + lista_claves_2[1]
    clave3 = lista_claves_1[2] + lista_claves_2[2]
    clave4 = lista_claves_1[3] + lista_claves_2[3]
    clave5 = lista_claves_1[4] + lista_claves_2[4]

    return clave1, clave2, clave3, clave4, clave5, mensaje_codificado


# En base a las claves recuperadas, se generan las listas de caracteres aleatorias como se usaron en el proceso de codificacion.
def recuperar_abc_lista_m(abc_tupla, clave):

    abc_lista = list(abc_tupla)
    abc_lista_modificada = []
    contador_c = 0
    contador_i = 1
    indice = ''
           
    for c in clave:
        
        if contador_i != 174:

            if contador_c == 2:
                abc_lista_modificada.append(abc_lista.pop(int(indice)))
                contador_c = 0
                indice = ''
                indice += c
            else:
                indice += c
                
            contador_c +=1
            contador_i +=1
        
        else:
            indice += c
            abc_lista_modificada.append(abc_lista.pop(int(indice)))

    return abc_lista_modificada


# A medida que se recupera cada lista modificada, se genera el diccionario correspondiente.
def recuperar_diccionario(abc_lista_modificada):
    
    diccionario = {}
    codigo = 1

    for c in abc_lista_modificada:
              
            valor = f'{codigo:02}'
            diccionario[valor] = c
            codigo += 1   
    
    return diccionario


# Habiendo recuperado los 5 diccionarios, se procede a la decodificación del mensaje.
def decodificar_mensaje(diccionario1, diccionario2, diccionario3, diccionario4, diccionario5, mensaje_codificado):

    diccionarios = (diccionario1, diccionario2, diccionario3, diccionario4, diccionario5)
    rotador = 0
    contador_c = 0
    key = ''
    mensaje_decodificado = ''
    mensaje_codificado = str(mensaje_codificado)
    longitud_mensaje = len(mensaje_codificado)
    
    for c in mensaje_codificado: 
                      
            if c.isdigit():
                if longitud_mensaje  != 1:    
                        if contador_c == 2:
                            mensaje_decodificado = mensaje_decodificado + diccionarios[rotador][key]      
                            contador_c = 0
                            key = ''
                            key += c
                            rotador = (rotador + 1) % len(diccionarios)

                        else:
                            key += c    

                        contador_c +=1
                        longitud_mensaje -= 1
                else:
                    key = key + c
                    mensaje_decodificado += diccionarios[rotador][key]

            else:
                if contador_c == 2:
                    mensaje_decodificado += diccionarios[rotador][key] 
                    mensaje_decodificado += c
                    contador_c = 0
                    key = ''
                    rotador = (rotador + 1) % len(diccionarios)
                else:
                    mensaje_decodificado += c
                longitud_mensaje -= 1

    print('\nDecoded message:', mensaje_decodificado)

#Función integradora para codificar
def codificar():
    abc_tupla =(':','R','S','T','U','V','W','u','(',')','v','w','x','y','z','2','$','3','4','5','6','7','G','H','!','I','J','K','L','j','k','l','m','n','ñ','?','á','é','í','ó','ú','Á','8','9','É','Í',' ','Ó','Ú','0','1','A','B','C','¿','D','E','F','d','e','f','g','¡','h','"','i','M','N',';','Ñ','O','P','Q','X',',','Y','Z','a','b','c','o','.','p','q','r','s','t')
    mascara = ('A','B','C','D','E','F','G','H','I','J','K','L','M','N','Ñ','O','P','Q','R','S','T','U','V','W','X','Y','Z','a','b','c','d','e','f','g','h','i','j','k','l','m','n','ñ','o','p','q','r','s','t','u','v','w','x','y','z',' ')
    abc_lista_modificada = []
    diccionario1 = {}
    clave1 = ''
    diccionario2 = {}
    clave2 = ''
    diccionario3 = {}
    clave3 = ''
    diccionario4 = {}
    clave4 = ''
    diccionario5 = {}
    clave5 = ''
    mensaje_codificado = ''
    
    abc_lista_modificada, clave1 = randomizar_abc_lista(abc_tupla)
    diccionario1 = generar_diccionario(abc_lista_modificada)
    abc_lista_modificada, clave2 = randomizar_abc_lista(abc_tupla)
    diccionario2 = generar_diccionario(abc_lista_modificada)
    abc_lista_modificada, clave3 = randomizar_abc_lista(abc_tupla)
    diccionario3 = generar_diccionario(abc_lista_modificada)
    abc_lista_modificada, clave4 = randomizar_abc_lista(abc_tupla)
    diccionario4 = generar_diccionario(abc_lista_modificada)
    abc_lista_modificada, clave5 = randomizar_abc_lista(abc_tupla)
    diccionario5 = generar_diccionario(abc_lista_modificada)
    
    mensaje_codificado = codificar_mensaje(diccionario1, diccionario2, diccionario3, diccionario4, diccionario5, abc_tupla)

    exportar(clave1, clave2, clave3, clave4, clave5, mensaje_codificado, mascara)

#Función integradora para decodificar
def decodificar():
    abc_tupla =(':','R','S','T','U','V','W','u','(',')','v','w','x','y','z','2','$','3','4','5','6','7','G','H','!','I','J','K','L','j','k','l','m','n','ñ','?','á','é','í','ó','ú','Á','8','9','É','Í',' ','Ó','Ú','0','1','A','B','C','¿','D','E','F','d','e','f','g','¡','h','"','i','M','N',';','Ñ','O','P','Q','X',',','Y','Z','a','b','c','o','.','p','q','r','s','t')
    mascara = ('A','B','C','D','E','F','G','H','I','J','K','L','M','N','Ñ','O','P','Q','R','S','T','U','V','W','X','Y','Z','a','b','c','d','e','f','g','h','i','j','k','l','m','n','ñ','o','p','q','r','s','t','u','v','w','x','y','z',' ')
    abc_lista_modificada = []
    diccionario1 = {}
    clave1 = ''
    diccionario2 = {}
    clave2 = ''
    diccionario3 = {}
    clave3 = ''
    diccionario4 = {}
    clave4 = ''
    diccionario5 = {}
    clave5 = ''
    mensaje_codificado = importar(mascara)
    
    clave1, clave2, clave3, clave4, clave5, mensaje_codificado = recuperar_claves(mensaje_codificado)

    abc_lista_modificada = recuperar_abc_lista_m(abc_tupla, clave1)
    diccionario1 = recuperar_diccionario(abc_lista_modificada)
    abc_lista_modificada = recuperar_abc_lista_m(abc_tupla, clave2)
    diccionario2 = recuperar_diccionario(abc_lista_modificada)
    abc_lista_modificada = recuperar_abc_lista_m(abc_tupla, clave3)
    diccionario3 = recuperar_diccionario(abc_lista_modificada)
    abc_lista_modificada = recuperar_abc_lista_m(abc_tupla, clave4)
    diccionario4 = recuperar_diccionario(abc_lista_modificada)
    abc_lista_modificada = recuperar_abc_lista_m(abc_tupla, clave5)
    diccionario5 = recuperar_diccionario(abc_lista_modificada)  

    decodificar_mensaje(diccionario1, diccionario2, diccionario3, diccionario4, diccionario5, mensaje_codificado)

    input('\nContinue (Enter)')


def menu():
    
    while True:
        system('cls')
        print('\nInput option:\n---------------\nCode: 1\nDecode: 2\nQuit: Enter')
        opcion = input()

        if opcion == '1':
            codificar()

        elif opcion == '2':
            decodificar()

        else:
            break

menu()