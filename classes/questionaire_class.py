import json
import os
import datetime
import tkinter as tk
from tkinter import messagebox, filedialog
from random import choice

class Questionaire:
    def __init__(self, qfile, shuffle):
        self.qfile = qfile
        self.shuffle = shuffle

        #% Variables para referenciar los resultados de las preguntas de test anteriores     
        self.correcto = 0
        self.fallado = 0
        self.blanco = 0

        #% Variables para referenciar los resultados de las preguntas de test actuales
        self.correcto_actual = 0
        self.fallado_actual = 0
        self.blanco_actual = 0

        #% Listas para guardar las preguntas falladas/blanco y la respuesta dada
        self.id_fallado = []
        self.contestado = []
    
    def results_manager(self, respuesta, pregunta):
        if self.shuffle.flag_shuffle == False:                  #NORMAL MODE
            solucion_correcta = pregunta["solution"]
        else:                                           #SUFFLE MODE
            solucion_correcta = self.shuffle.solucion_mezclada

        if respuesta == solucion_correcta:
            self.correcto += 1
            self.correcto_actual += 1
        elif respuesta == "":
            self.blanco += 1
            self.blanco_actual += 1
            self.id_fallado += [self.qfile.current_question]
            self.contestado += [(self.qfile.current_question,"BLANCO")]
            if self.shuffle.flag_shuffle:
                self.shuffle.solucion_mezclada_lista += [(self.qfile.current_question, self.shuffle.solucion_mezclada)]
        else:
            self.fallado += 1
            self.fallado_actual += 1
            self.id_fallado += [self.qfile.current_question]
            self.contestado += [(self.qfile.current_question,respuesta)]
            if self.shuffle.flag_shuffle:
                self.shuffle.solucion_mezclada_lista += [(self.qfile.current_question, self.shuffle.solucion_mezclada)]