import json
import os
import datetime
import tkinter as tk
from tkinter import messagebox, filedialog
from random import choice

class PreviousTest:
    def __init__(self, init, questionaire, shuffle, qfile, frame_manager):
        self.frame_manager = frame_manager
        self.questionaire = questionaire
        self.init = init
        self.shuffle = shuffle
        self.qfile = qfile

        self.flag_pmode = False
        self.file_path = None
        
    def off_pflag(self):
        self.flag_pmode = False
        self.frame_manager.prev_test_path.config(text="Select the previous test file")

        self.qfile.lineas = None
        self.qfile.preguntas_realizadas = []
        self.shuffle.flag_shuffle = self.shuffle.flag_shuffle_interno
        self.questionaire.correcto = 0
        self.questionaire.blanco = 0
        self.questionaire.fallado = 0
        self.qfile.nombre_test_anterior = ""


    def on_pflag(self):
        self.flag_pmode = True

    def set_previous_test_path(self):
        self.file_path = filedialog.askopenfilename(initialdir=os.path.join(self.init.root_path, "TESTS ANTERIORES"), 
                                                  title="Seleccionar archivo previo",
                                                  filetypes=(("Archivos de texto", "*.txt"),))
        self.frame_manager.prev_test_path.config(text=self.file_path)
        self.on_pflag()
    
    def load_previous_test(self):
        # if messagebox.askyesno("Continuar", "¿Desea continuar con un test previo?"):
            self.set_previous_test_path()
            if self.file_path:
                if self.qfile.nombre_fichero_preguntas[:-5] not in self.file_path:
                    messagebox.showerror("Error", "El archivo seleccionado no pertenece al fichero de preguntas seleccionado")
                    while self.qfile.nombre_fichero_preguntas[:-5] not in self.file_path:
                        self.file_path = filedialog.askopenfilename(initialdir=os.path.join(self.init.root_path, "TESTS ANTERIORES"), 
                                                  title="Seleccionar archivo previo",
                                                  filetypes=(("Archivos de texto", "*.txt"),))
                        if not self.file_path:
                            break
                        elif self.qfile.nombre_fichero_preguntas[:-5] not in self.file_path:
                            messagebox.showerror("Error", "El archivo seleccionado no pertenece al fichero de preguntas seleccionado")
                if not self.file_path: #EN CASO DE CANCELAR
                    raise SystemExit
                else:
                    with open(self.file_path, "r") as f:
                        lineas = f.readlines()
                        self.qfile.lineas = lineas
                        self.qfile.preguntas_realizadas = [int(i.translate({ord(c): None for c in '[,]'})) for i in lineas[4].split()]
                        self.shuffle.flag_shuffle = bool(int(lineas[2].split()[-1]))
                        self.questionaire.correcto = int(lineas[5].split()[0].translate({ord(c): None for c in '[,]'}))
                        self.questionaire.blanco = int(lineas[5].split()[1].translate({ord(c): None for c in '[,]'}))
                        self.questionaire.fallado = int(lineas[5].split()[2].translate({ord(c): None for c in '[,]'}))
                        # self.frame_manager.status_label.config(text=f"Estado: {self.questionaire.correcto} correctos, {self.questionaire.fallado} fallados, {self.questionaire.blanco} en blanco")
                        self.qfile.nombre_test_anterior = os.path.basename(self.file_path)
        # else: #EN EL CASO DE NO QUERER HACER UN TEST PREVIO, SE PREGUNTA SI QUIERE LAS OPCIONES MEZCLADAS
        #     self.shuffle.flag_shuffle = bool(int(messagebox.askyesno("Shuffle", "¿Desea activar el modo shuffle?")))
        # #Cambio estético para poder visualizar en la ventana el test que se está realizando y si tiene las opciones mezcladas
        # self.init.root.title(f"Test de Preguntas [Test: {self.qfile.nombre_fichero_preguntas[:-5]}] [Shuffle: {"ON" if int(self.shuffle.flag_shuffle) == 1 else "OFF"}]")   
 