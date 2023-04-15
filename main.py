# -*- coding: utf-8 -*-
# Module: pyopenai
# Created on: 14/04/2023
# Authors: -∞WKS∞-#3982
# Version: 1.0.0

import openai
import os
import logging

# Configurar el logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

# Función para obtener la clave de API de OpenAI
def obtener_api_key():
    api_key = "Your ApiKey"
    if api_key is None:
        logger.error("No se ha encontrado la clave de API de OpenAI en las variables de entorno.")
        return None
    else:
        return api_key

# Función para generar un archivo de script de Python
def generar_script_python(mensaje, respuesta):
    # Generar el nombre de archivo
    file_name = "file_generate{}.py".format(len(os.listdir()) + 1)
    # Crear el archivo y escribir el contenido
    with open(file_name, "w") as f:
        f.write('"""Script generado automáticamente por OpenAI"""\n\n')
        f.write('mensaje = """{}"""\n\n'.format(mensaje))
        f.write('respuesta = """{}"""\n\n'.format(respuesta))
        f.write('print("Mensaje recibido:")\n')
        f.write('print(mensaje)\n\n')
        f.write('print("Respuesta generada:")\n')
        f.write('print(respuesta)\n')
        logger.info("Archivo generado exitosamente: %s", file_name)

# Función para iniciar sesión en OpenAI
def login(api_key):
    if api_key is not None:
        openai.api_key = api_key
        logger.info("Inicio de sesión exitoso. Tu clave de API de OpenAI ha sido guardada.")
    else:
        logger.error("No se pudo iniciar sesión en OpenAI.")

# Función para generar respuesta a partir de un mensaje
def generar_respuesta(mensaje):
    response = openai.Completion.create(
        engine="davinci",
        prompt=mensaje,
        max_tokens=60,
        n=1,
        stop=None,
        temperature=0.7,
    )

    return response.choices[0].text.strip()

# Función para guardar respuestas en un archivo de texto
def guardar_respuesta(respuesta):
    with open("respuestas.txt", "a") as f:
        f.write(respuesta + "\n")

# Función para leer y mostrar respuestas guardadas en un archivo de texto
def mostrar_respuestas_guardadas():
    if os.path.isfile("respuestas.txt"):
        with open("respuestas.txt", "r") as f:
            respuestas = f.read().splitlines()
        if len(respuestas) > 0:
            logger.info("Respuestas guardadas:")
            for respuesta in respuestas:
                logger.info("- %s", respuesta)
        else:
            logger.info("No hay respuestas guardadas aún.")
    else:
        logger.error("No se encontró el archivo de respuestas.")

# Pedir clave de API de OpenAI al usuario
api_key = obtener_api_key()

# Iniciar sesión en OpenAI
login(api_key)

# Pedir mensaje de entrada al usuario
mensaje = input("Escribe tu mensaje: ")

# Generar respuesta
respuesta_generada = generar_respuesta(mensaje)

# Guardar respuesta en archivo de texto
guardar_respuesta(respuesta_generada)

# Preguntar si se desea continuar usando la respuesta generada
while True:
    continuar = input("¿Deseas continuar y usar la respuesta generada? (y/n)")
    if continuar.lower() == 'y':
        # Guardar respuesta en archivo de texto
        guardar_respuesta(respuesta_generada)

        # Preguntar si se desea generar un nuevo archivo de script
        while True:
            generar_script = input("¿Deseas generar un nuevo archivo de script? (y/n)")
            if generar_script.lower() == 'y':
                # Generar nuevo archivo de script
                numero_archivo += 1
                nombre_archivo = f"file_generate{numero_archivo}.py"
                with open(nombre_archivo, "w") as f:
                    f.write(respuesta_generada)
                print(f"Archivo generado exitosamente: {nombre_archivo}")
                break
            elif generar_script.lower() == 'n':
                # Mostrar respuestas guardadas y terminar el programa
                mostrar_respuestas_guardadas()
                logger.info("Programa finalizado")
                break
            else:
                print("Respuesta no válida. Por favor ingresa 'y' o 'n'")
        break
    elif continuar.lower() == 'n':
        # Mostrar respuestas guardadas y terminar el programa
        mostrar_respuestas_guardadas()
        logger.info("Programa finalizado")
        break
    else:
        print("Respuesta no válida. Por favor ingresa 'y' o 'n'")
