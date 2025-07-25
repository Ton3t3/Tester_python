import json
import os
import datetime
import tkinter as tk
from tkinter import messagebox, filedialog
from random import choice
from PIL import Image, ImageTk


class Question_file:
    def __init__(self, init, questionaire, shuffle, smode, frame_manager, prev_test, e2json):
        self.init = init
        self.questionaire = questionaire
        self.shuffle = shuffle
        self.smode = smode
        self.frame_manager = frame_manager
        self.prev_test = prev_test
        self.excel_to_json = e2json

        
        self.root_fichero_preguntas = None      # Nombre del fichero de preguntas
        self.nombre_fichero_preguntas = ""    # Dirección del fichero de preguntas

        self.root_fichero_imagenes = ""       # Nombre del directorio de imagenes
        self.uso_de_imgs = True     

        self.data = None                        # Carga el fichero de preguntas
        self.num_preguntas = 0
        self.num_preguntas_totales = 0         # Número de preguntas totales en el fichero
        self.num_opciones_preguntas = 0         # Número de preguntas totales en el test
        self.test_names = None
        self.num_preguntas_per_test = None
        self.test_title = ""

        self.opciones_preguntas = []
        self.alfabeto = ["a", "b", "c", "d", "e", "f", "g"]

        self.nombre_test_anterior = ""          # Contiene el nombre del fichero del test anterior, sirviendo también como flag para saber si se ha realizado un test previo
        self.preguntas_realizadas = []
        self.current_question = None            # Variable donde se guardará el valor de la respuesta escogida por la función choose
        self.lineas = None                      # Variable donde se alojarán las líneas del fichero de respuesta del test anterior

    def load_question_file(self):
        self.root_fichero_preguntas = filedialog.askopenfilename(initialdir=os.path.join(self.init.root_path), 
                                                  title="Seleccionar fichero de preguntas",
                                                  filetypes=(("Archivos de texto", "*.json"),("Excel files", "*.xlsx")))   
                                             
        self.nombre_fichero_preguntas = os.path.basename(self.root_fichero_preguntas)
        self.data = self.load_data()      
        self.num_preguntas_totales = len(self.data['emp_details'])
        self.num_opciones_preguntas = len(self.data['emp_details'][0]['options'][0])
        self.frame_manager.question_file_path.config(text=self.nombre_fichero_preguntas)      
        self.opciones_preguntas = []

        for i in range(0,self.num_opciones_preguntas):
            self.opciones_preguntas.append(self.alfabeto[i])

        [self.test_names, self.num_preguntas_per_test] = self.get_test_names(self.data, self.num_preguntas_totales)
        self.frame_manager.combo.config(values=self.test_names)
        self.frame_manager.combo.current(0)
        
        self.num_preguntas = len(self.data['emp_details'])
        self.frame_manager.number_of_questions_label.config(text=f"Número de preguntas: {self.num_preguntas}")
        if self.prev_test.flag_pmode:
            self.prev_test.off_pflag()     #Borra el test previo si se ha seleccionado un nuevo test de preguntas

    def get_test_names(self, data, num_preguntas_totales):
        output_array = ["All tests"]
        raw_output_array = []
        for i in range(0, num_preguntas_totales):
            if data['emp_details'][i]['test'] not in output_array:
                output_array.append(data['emp_details'][i]['test'])
            raw_output_array.append(data['emp_details'][i]['test'])
            num_preguntas_per_test = []
            for j in range(1,len(output_array)):
                aux = raw_output_array.count(output_array[j])
                num_preguntas_per_test.append(aux)
        return output_array, num_preguntas_per_test

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

        if self.test_title == "":
            self.test_title = self.frame_manager.combo.get()
            self.set_num_preguntas()

        if len(self.preguntas_realizadas) >= self.num_preguntas:
            if self.smode.flag_smode == False:
                self.questionaire.end_test()
                return
            else:
                self.smode.smode_end_test()
                return
        if self.test_title == "All tests":
            self.current_question = choice([i for i in range(self.num_preguntas_totales) if (i not in self.preguntas_realizadas)])
        else:
            self.current_question = choice([i for i in range(self.num_preguntas_totales) if ((i not in self.preguntas_realizadas) and (self.data['emp_details'][i]['test'] == self.test_title))])
        pregunta = self.data['emp_details'][self.current_question]
        
        self.frame_manager.question_label.config(text=pregunta["question"]) if not self.smode.flag_smode else self.frame_manager.study_question_label.config(text=pregunta["question"])
        self.frame_manager.question_id_label.config(text=f"Respondidas: {len(self.preguntas_realizadas)}/{self.num_preguntas}") if not self.smode.flag_smode else self.frame_manager.study_question_id_label.config(text=f"Respondidas: {len(self.preguntas_realizadas)}/{self.num_preguntas}")

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

    def set_num_preguntas(self):
        if self.test_title == "All tests" or self.test_title == "":
            self.num_preguntas = len(self.data['emp_details'])
            # print(f"Num preguntas para test All tests: {self.num_preguntas}")
        else:
            for i in range(1, len(self.test_names)):
                if self.test_title == self.test_names[i]:
                    self.num_preguntas = self.num_preguntas_per_test[i-1]
                    # print(f"Num preguntas para test {self.qfile.test_names[i]}: {self.qfile.num_preguntas}")
                    break
        self.frame_manager.number_of_questions_label.config(text=f"Total questions: {self.num_preguntas}")

    def load_data(self):
        if self.root_fichero_preguntas.endswith('.xlsx'):
            self.excel_to_json.excel_url = self.root_fichero_preguntas
            fichero_json = self.excel_to_json.generate_json()
            return fichero_json
        else:
            with open(os.path.join(self.root_fichero_preguntas), "r",encoding="utf-8") as f:
                return json.load(f)