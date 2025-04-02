import json
import os
import datetime
import tkinter as tk
from tkinter import messagebox, filedialog
from random import choice

class Questionaire:
    def __init__(self, qfile):
        self.qfile = qfile

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
    