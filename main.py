import heapq
import os
import sys
from collections import Counter

class Nodo:
    def __init__(self, car=None, freq=0, izq=None, der=None):
        self.car = car
        self.freq = freq
        self.izq = izq
        self.der = der

    def __lt__(self, other):
        return self.freq < other.freq


def leer_archivo(archivo):
    ruta_archivo = os.path.join(os.getcwd(), archivo)
    with open(ruta_archivo, 'r') as file:
        contenido = file.read()
        print("Contenido del archivo:", contenido)  # Agregar esta línea para verificar el contenido del archivo
        return contenido


def calcular_frecuencias(texto):
    frecuencias = dict(Counter(texto))
    return {str(car): str(freq) for car, freq in frecuencias.items()}



def construir_arbol(frecuencias):
    cola_prioridad = [Nodo(car, freq) for car, freq in frecuencias.items()]
    heapq.heapify(cola_prioridad)

    while len(cola_prioridad) > 1:
        nodo_izq = heapq.heappop(cola_prioridad)
        nodo_der = heapq.heappop(cola_prioridad)
        nodo_padre = Nodo(freq=nodo_izq.freq + nodo_der.freq, izq=nodo_izq, der=nodo_der)
        heapq.heappush(cola_prioridad, nodo_padre)

    return cola_prioridad[0]


def asignar_codigos(arbol, codigo_actual, codigos):
    if arbol.car:
        codigos[arbol.car] = codigo_actual
    else:
        asignar_codigos(arbol.izq, codigo_actual + "0", codigos)
        asignar_codigos(arbol.der, codigo_actual + "1", codigos)


def codificar_texto(texto, codigos):
    return ''.join(format(ord(car), '08b') for car in texto)



def escribir_archivo_comprimido(texto_codificado, frecuencias, archivo_salida):
    # Convertir las frecuencias en formato de texto en un diccionario de enteros
    frecuencias = {car: int(freq) for car, freq in frecuencias.items()}

    # Crear una cadena que contenga la representación de las frecuencias en formato 'car:freq;'
    frecuencias_str = ';'.join(f"{car}:{freq}" for car, freq in frecuencias.items())

    # Concatenar las frecuencias y el texto codificado en una sola cadena separada por '#'
    datos_comprimidos = f"{frecuencias_str}#{texto_codificado}"

    # Convertir la cadena binaria en una secuencia de bytes
    bytes_comprimidos = datos_comprimidos.encode()

    # Escribir los bytes comprimidos en el archivo de salida en modo binario ('wb')
    with open(archivo_salida, 'wb') as file:
        file.write(bytes_comprimidos)



def decodificar_archivo(archivo_comprimido):
    with open(archivo_comprimido, 'rb') as file:
        bytes_comprimidos = file.read()

    # Convertir la secuencia de bytes en una cadena binaria
    datos_comprimidos = bytes_comprimidos.decode()

    # Obtener las frecuencias y el texto codificado de la cadena binaria
    separador_index = datos_comprimidos.index('#')  # Buscamos el carácter '#' como separador
    frecuencias_str = datos_comprimidos[:separador_index]
    texto_codificado = datos_comprimidos[separador_index + 1:]

    # Convertir las frecuencias en formato de texto a un diccionario de enteros
    frecuencias = {}
    for item in frecuencias_str.split(';'):
        car, freq = item.split(':')
        frecuencias[car] = int(freq)

    # Construir el árbol de Huffman usando las frecuencias
    arbol = construir_arbol(frecuencias)

    # Decodificar el texto codificado
    texto_decodificado = ""
    nodo_actual = arbol
    for bit in texto_codificado:
        if bit == '0':
            nodo_actual = nodo_actual.izq
        else:
            nodo_actual = nodo_actual.der

        if nodo_actual.car:
            texto_decodificado += nodo_actual.car
            nodo_actual = arbol

    return texto_decodificado



def escribir_archivo_decodificado(texto_decodificado, archivo_salida):
    with open(archivo_salida, 'w') as file:
        file.write(texto_decodificado)


def calcular_tasa_compresion(archivo_original, archivo_comprimido):
    tamano_original = os.path.getsize(archivo_original)
    tamano_comprimido = os.path.getsize(archivo_comprimido)
    tasa_compresion = (tamano_comprimido / tamano_original) * 100
    return tasa_compresion


# Ejemplo de uso

# Obtener la ruta absoluta del archivo actualmente en ejecución
ruta_actual = os.path.abspath(__file__)

# Obtener la ruta del directorio del archivo
directorio_actual = os.path.dirname(ruta_actual)

# Construir la ruta completa del archivo "archivo.txt"
archivo_entrada = os.path.join(directorio_actual, "archivo.txt")
archivo_comprimido = os.path.join(directorio_actual, "archivo_comprimido.bin")
archivo_decodificado = os.path.join(directorio_actual, "archivo_decodificado.txt")

# Paso 1: Lectura del archivo de entrada
texto_original = leer_archivo(archivo_entrada)

# Paso 2: Cálculo de frecuencias
frecuencias = calcular_frecuencias(texto_original)

# Paso 3: Construcción del árbol de Huffman
arbol_huffman = construir_arbol(frecuencias)

# Paso 4: Asignación de códigos
codigos = {}
asignar_codigos(arbol_huffman, "", codigos)

# Paso 5: Codificación del archivo de texto
texto_codificado = codificar_texto(texto_original, codigos)

# Paso adicional: Convertir las frecuencias en formato de texto a un diccionario de enteros
frecuencias = {car: int(freq) for car, freq in frecuencias.items()}

# Paso 6: Escritura del archivo comprimidos
escribir_archivo_comprimido(texto_codificado, frecuencias, archivo_comprimido)

# Paso 7: Decodificación del archivo comprimido
texto_decodificado = decodificar_archivo(archivo_comprimido)

# Paso 8: Escritura del archivo decodificado
escribir_archivo_decodificado(texto_decodificado, archivo_decodificado)

# Paso 9: Cálculo de la tasa de compresión
tasa_compresion = calcular_tasa_compresion(archivo_entrada, archivo_comprimido)

# Imprimir los resultados
print("Texto codificado:", texto_codificado)
print("Texto decodificado:", texto_decodificado)
print("Tasa de compresión:", tasa_compresion)
