import json
import os
import datetime
import tkinter as tk
from tkinter import messagebox, filedialog
from random import choice

class PreviousTest:
    def __init__(self, init, questionaire, shuffle, widget, qfile):
        self.questionaire = questionaire
        self.init = init
        self.shuffle = shuffle
        self.widget = widget
        self.qfile = qfile
        
    def load_previous_test(self):
        if messagebox.askyesno("Continuar", "¿Desea continuar con un test previo?"):
            file_path = filedialog.askopenfilename(initialdir=os.path.join(self.init.root_path, "TESTS ANTERIORES"), 
                                                  title="Seleccionar archivo previo",
                                                  filetypes=(("Archivos de texto", "*.txt"),))
            if file_path:
                if self.qfile.nombre_fichero_preguntas[:-5] not in file_path:
                    messagebox.showerror("Error", "El archivo seleccionado no pertenece al fichero de preguntas seleccionado")
                    while self.qfile.nombre_fichero_preguntas[:-5] not in file_path:
                        file_path = filedialog.askopenfilename(initialdir=os.path.join(self.init.root_path, "TESTS ANTERIORES"), 
                                                  title="Seleccionar archivo previo",
                                                  filetypes=(("Archivos de texto", "*.txt"),))
                        if not file_path:
                            break
                        elif self.qfile.nombre_fichero_preguntas[:-5] not in file_path:
                            messagebox.showerror("Error", "El archivo seleccionado no pertenece al fichero de preguntas seleccionado")
                if not file_path: #EN CASO DE CANCELAR
                    raise SystemExit
                else:
                    with open(file_path, "r") as f:
                        lineas = f.readlines()
                        self.qfile.lineas = lineas
                        self.qfile.preguntas_realizadas = [int(i.translate({ord(c): None for c in '[,]'})) for i in lineas[4].split()]
                        self.shuffle.flag_shuffle = bool(int(lineas[2].split()[-1]))
                        self.questionaire.correcto = int(lineas[5].split()[0].translate({ord(c): None for c in '[,]'}))
                        self.questionaire.blanco = int(lineas[5].split()[1].translate({ord(c): None for c in '[,]'}))
                        self.questionaire.fallado = int(lineas[5].split()[2].translate({ord(c): None for c in '[,]'}))
                        self.widget.status_label.config(text=f"Estado: {self.questionaire.correcto} correctos, {self.questionaire.fallado} fallados, {self.questionaire.blanco} en blanco")
                        self.qfile.nombre_test_anterior = os.path.basename(file_path)
        else: #EN EL CASO DE NO QUERER HACER UN TEST PREVIO, SE PREGUNTA SI QUIERE LAS OPCIONES MEZCLADAS
            self.shuffle.flag_shuffle = bool(int(messagebox.askyesno("Shuffle", "¿Desea activar el modo shuffle?")))
        #Cambio estético para poder visualizar en la ventana el test que se está realizando y si tiene las opciones mezcladas
        self.init.root.title(f"Test de Preguntas [Test: {self.qfile.nombre_fichero_preguntas[:-5]}] [Shuffle: {"ON" if int(self.shuffle.flag_shuffle) == 1 else "OFF"}]")   
 