import json
import os
import datetime
import tkinter as tk
from tkinter import messagebox, filedialog
from random import choice


def load_data(root_fichero_preguntas):
        with open(os.path.join(root_fichero_preguntas), "r",encoding="utf-8") as f:
            return json.load(f)

class Question_file:
    def __init__(self, init, questionaire, shuffle, smode, frame_manager):
        self.init = init
        self.questionaire = questionaire
        self.shuffle = shuffle
        self.smode = smode
        self.frame_manager = frame_manager

        # Nombre del fichero de preguntas
        self.root_fichero_preguntas = filedialog.askopenfilename(initialdir=os.path.join(self.init.root_path), 
                                                  title="Seleccionar fichero de preguntas",
                                                  filetypes=(("Archivos de texto", "*.json"),))   
                                             
        # Dirección del fichero de preguntas
        self.nombre_fichero_preguntas = os.path.basename(self.root_fichero_preguntas)

        self.data = load_data(self.root_fichero_preguntas)      # Carga el fichero de preguntas
        self.num_preguntas = len(self.data['emp_details'])
        self.num_opciones_preguntas = len(self.data['emp_details'][0]['options'][0])      # Número de preguntas totales en el test

        self.opciones_preguntas = []
        alfabeto = ["a", "b", "c", "d", "e", "f", "g"]
        for i in range(0,self.num_opciones_preguntas):
            self.opciones_preguntas.append(alfabeto[i])

        self.nombre_test_anterior = ""                          # Contiene el nombre del fichero del test anterior, sirviendo también como flag para saber si se ha realizado un test previo
        
        self.preguntas_realizadas = []
        self.current_question = None    # Variable donde se guardará el valor de la respuesta escogida por la función choose
        self.lineas = None                                      # Variable donde se alojarán las líneas del fichero de respuesta del test anterior


    def display_question(self):
        if len(self.preguntas_realizadas) >= self.num_preguntas:
            if self.smode.flag_smode == False:
                self.questionaire.end_test()
                return
            else:
                self.smode.smode_end_test()
                return

        self.current_question = choice([i for i in range(self.num_preguntas) if i not in self.preguntas_realizadas])
        pregunta = self.data['emp_details'][self.current_question]
        
        self.frame_manager.question_label.config(text=pregunta["question"]) if not self.smode.flag_smode else self.frame_manager.study_question_label.config(text=pregunta["question"])
        opciones = pregunta["options"][0]
        

        if not self.shuffle.flag_shuffle:
            preguntas = self.opciones_preguntas
        else:            
            letras_preguntas_mezcladas = self.shuffle.mezclador_letras(self.opciones_preguntas, pregunta, self.opciones_preguntas)
            preguntas = letras_preguntas_mezcladas

        for i, key in enumerate(preguntas):
            self.frame_manager.options_buttons[i].config(text=f"{key}: {opciones[key]}") if not self.smode.flag_smode else self.frame_manager.study_options_buttons[i].config(text=f"{key}: {opciones[key]}")
        self.frame_manager.options_var.set("") if not self.smode.flag_smode else self.frame_manager.study_options_var.set("")
    