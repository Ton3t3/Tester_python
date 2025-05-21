import json
import os
import datetime
import tkinter as tk
from tkinter import messagebox, filedialog
from random import choice
from PIL import Image, ImageTk


def load_data(root_fichero_preguntas):
        with open(os.path.join(root_fichero_preguntas), "r",encoding="utf-8") as f:
            return json.load(f)

class Question_file:
    def __init__(self, init, questionaire, shuffle, smode, frame_manager, prev_test):
        self.init = init
        self.questionaire = questionaire
        self.shuffle = shuffle
        self.smode = smode
        self.frame_manager = frame_manager
        self.prev_test = prev_test

        
        self.root_fichero_preguntas = None      # Nombre del fichero de preguntas
        self.nombre_fichero_preguntas = ""    # Dirección del fichero de preguntas

        self.root_fichero_imagenes = ""       # Nombre del directorio de imagenes
        self.uso_de_imgs = True     

        self.data = None                        # Carga el fichero de preguntas
        self.num_preguntas = 0
        self.num_opciones_preguntas = 0         # Número de preguntas totales en el test

        self.opciones_preguntas = []
        self.alfabeto = ["a", "b", "c", "d", "e", "f", "g"]

        self.nombre_test_anterior = ""          # Contiene el nombre del fichero del test anterior, sirviendo también como flag para saber si se ha realizado un test previo
        self.preguntas_realizadas = []
        self.current_question = None            # Variable donde se guardará el valor de la respuesta escogida por la función choose
        self.lineas = None                      # Variable donde se alojarán las líneas del fichero de respuesta del test anterior

    def load_question_file(self):
        self.root_fichero_preguntas = filedialog.askopenfilename(initialdir=os.path.join(self.init.root_path), 
                                                  title="Seleccionar fichero de preguntas",
                                                  filetypes=(("Archivos de texto", "*.json"),))   
                                             
        self.nombre_fichero_preguntas = os.path.basename(self.root_fichero_preguntas)

        self.data = load_data(self.root_fichero_preguntas)      
        self.num_preguntas = len(self.data['emp_details'])
        self.num_opciones_preguntas = len(self.data['emp_details'][0]['options'][0])
        self.frame_manager.question_file_path.config(text=self.nombre_fichero_preguntas)      

        for i in range(0,self.num_opciones_preguntas):
            self.opciones_preguntas.append(self.alfabeto[i])

        self.prev_test.off_pflag()     #Borra el test previo si se ha seleccionado un nuevo test de preguntas

    def load_image_folder(self):
        self.root_fichero_imagenes = filedialog.askdirectory(initialdir=os.path.join(self.init.root_path), 
                                                  title="Seleccionar directorio de imágenes")
        
        self.frame_manager.image_folder_path.config(text=self.root_fichero_imagenes)      

    def display_question(self):
        if self.nombre_fichero_preguntas == "":
            messagebox.showerror("Error", "No se ha seleccionado un fichero de preguntas")
            self.frame_manager.show_frame("init_frame")
            return

        if self.root_fichero_imagenes == "":
            for i in range(self.num_preguntas):
                if len(self.data['emp_details'][i]) == 4:
                    break
                if self.data['emp_details'][i]["image"][0]['img_bool'] == True:
                    messagebox.showerror("Error", "No se ha seleccionado un directorio de imágenes")
                    self.frame_manager.remove_frame("test_frame")
                    self.frame_manager.show_frame("init_frame")
                    return
            self.uso_de_imgs = False

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
        
        self.display_image(pregunta)

        if not self.shuffle.flag_shuffle:
            for i, key in enumerate(self.opciones_preguntas):
                self.frame_manager.options_buttons[i].config(text=f"{key}: {opciones[key]}") if not self.smode.flag_smode else self.frame_manager.study_options_buttons[i].config(text=f"{key}: {opciones[key]}")
        else:            
            letras_preguntas_mezcladas = self.shuffle.mezclador_letras(self.opciones_preguntas, pregunta, self.opciones_preguntas)
            for i, key in enumerate(letras_preguntas_mezcladas):
                self.frame_manager.options_buttons[i].config(text=f"{self.opciones_preguntas[i]}: {opciones[key]}") if not self.smode.flag_smode else self.frame_manager.study_options_buttons[i].config(text=f"{self.opciones_preguntas[i]}: {opciones[key]}")          
        
        self.frame_manager.adjust_canvas(self.frame_manager.current_canvas, self.frame_manager.current_frame)
        self.frame_manager.options_var.set("") if not self.smode.flag_smode else self.frame_manager.study_options_var.set("")
    
    def display_image(self, pregunta):
        if not self.uso_de_imgs:
            return
        else:
            bool_imagen = pregunta["image"][0]['img_bool']
            if bool_imagen == False or self.uso_de_imgs == False:
                if not self.smode.flag_smode:
                    self.frame_manager.question_image.config(image="")
                    self.frame_manager.question_image.image = None
                else:
                    self.frame_manager.study_question_image.config(image="")
                    self.frame_manager.study_question_image.image = None
            else:
                nombre_imagen = pregunta["image"][0]['img_name']
                imagen_select = Image.open(os.path.join(self.root_fichero_imagenes, nombre_imagen))
                test = ImageTk.PhotoImage(imagen_select)
                if not self.smode.flag_smode:
                    self.frame_manager.question_image.config(image=test)
                    self.frame_manager.question_image.image = test
                else:
                    self.frame_manager.study_question_image.config(image=test)
                    self.frame_manager.study_question_image.image = test