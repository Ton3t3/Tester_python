import json
import os
import datetime
import tkinter as tk
from tkinter import messagebox, filedialog
from random import choice


class Shuffle:
    def __init__(self):
        self.flag_shuffle = False                               # Flag para saber si está activo el modo shuffle
        self.solucion_mezclada_lista = []                       # Lista donde se guardarán los valores correctos de las preguntas erradas tras mezclar las opciones
        self.solucion_mezclada = ""                             # Variable donde se escribirá el resultado de la pregunta correcta tras mezclar las opciones (no es la misma letra del JSON)
    
    def mezclador_letras(self, letras_preguntas, pregunta, opciones_preguntas):
        letras_preguntas_usadas = []
        for i in range(0,len(opciones_preguntas)):
            # key tiene que ser random de entre a y d
            key = choice([j for j in opciones_preguntas if j not in letras_preguntas_usadas])
            # Hay que tener en cuenta el cambio de key hay que anotarlo para poder ser referenciado correctamente en la respuesta
            if  key == pregunta["solution"]:
                self.solucion_mezclada = letras_preguntas[i]
            letras_preguntas_usadas.append(key)
        return letras_preguntas_usadas