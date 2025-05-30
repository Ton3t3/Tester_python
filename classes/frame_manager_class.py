import json
import os
import datetime
import tkinter as tk
from tkinter import messagebox, filedialog, Frame, ttk
from random import choice
import random
import time
from PIL import Image, ImageTk


class FrameManager:
    def __init__(self, root, questionaire, qfile, shuffle, smode, prev_test, init):
        self.root = root
        self.questionaire = questionaire
        self.qfile = qfile 
        self.shuffle = shuffle
        self.smode = smode
        self.prev_test = prev_test
        self.init = init

        self.windows = {}
        self.current_window = None
        self.current_frame = None
        self.current_canvas = None

        self.question_label = None
        self.status_label = None
        self.options_buttons = None
        self.options_var = None
        self.question_image = None

        self.study_question_label = None
        self.study_status_label = None
        self.study_options_buttons = None
        self.study_options_var = None
        self.study_next_button = None
        self.study_previous_button = None
        self.study_percentage_correct_label = None
        self.study_percentage_incorrect_label = None
        self.study_question_image = None

    def add_frame(self, name:str):
        frame = Frame(self.root)
        self.windows[name] = frame
        if self.current_window is None:
            self.current_window = frame
            self.current_window.pack(fill="both", expand=True)
    
    def get_frame(self, name:str):
        return self.windows.get(name)

    def show_frame(self, name:str):
        if name in self.windows:
            if self.current_window is not None:
                self.current_window.pack_forget()
            self.current_window = self.windows[name]
            self.current_window.pack(fill="both", expand=True)

    def remove_frame(self, name:str):
        if name in self.windows:
            del self.windows[name]

    def init_frame(self):
        self.add_frame("init_frame")
        f = self.get_frame("init_frame")
        
        #Método para que la ventana sea scrollable
        init_canvas = tk.Canvas(f)
        init_canvas.pack(side="left", fill="both", expand=True)
        self.current_canvas = init_canvas
        y_scrollbar = ttk.Scrollbar(f, orient="vertical", command=init_canvas.yview)
        y_scrollbar.pack(side="right", fill="y")
        init_canvas.configure(yscrollcommand=y_scrollbar.set)
        init_canvas.bind("<Configure>", lambda e: init_canvas.configure(scrollregion=init_canvas.bbox("all")))

        init_frame_var = tk.Frame(init_canvas)
        init_canvas.create_window((0, 0), window=init_frame_var, anchor="nw")
        self.current_frame = init_frame_var

        question_file_frame = tk.Frame(init_frame_var)
        question_file_frame.pack(pady=10, anchor="center", fill="x")
        question_file_button = tk.Radiobutton(question_file_frame, text="Seleccionar fichero de preguntas", command=self.qfile.load_question_file)
        question_file_button.pack(side="left", padx=10)
        self.question_file_path = tk.Label(question_file_frame, text="Seleccionar fichero de preguntas", wraplength=400, justify="left")
        self.question_file_path.pack(side="left", padx=10)

        test_name_frame = tk.Frame(init_frame_var)
        test_name_frame.pack(pady=10, anchor="center", fill="x")
        test_name_label = tk.Label(test_name_frame, text="Seleccionar el test a realizar")
        test_name_label.pack(side="left", padx=10)
        self.combo = ttk.Combobox(test_name_frame, values=[], state="readonly")
        self.combo.pack(side="left", padx=10)
        self.combo.bind("<<ComboboxSelected>>", self.check_box)
        self.number_of_questions_label = tk.Label(test_name_frame, text="Número de preguntas: 0")
        self.number_of_questions_label.pack(side="left", padx=10)

        image_file_frame = tk.Frame(init_frame_var)
        image_file_frame.pack(pady=10, anchor="center", fill="x")
        image_file_button = tk.Radiobutton(image_file_frame, text="Seleccionar directorio de imágenes", command=self.qfile.load_image_folder)
        image_file_button.pack(side="left", padx=10)
        self.image_folder_path = tk.Label(image_file_frame, text="Seleccionar directorio de imágenes", wraplength=400, justify="left")
        self.image_folder_path.pack(side="left", padx=10)

        studio_button = tk.Checkbutton(init_frame_var, text="Modo Estudio", command=lambda:self.smode.turn_sflag(), onvalue=True, offvalue=False)
        studio_button.pack(pady=10)

        shuffle_button = tk.Checkbutton(init_frame_var, text="Modo Shuffle", command=lambda:self.shuffle.turn_shuffle_flag(), onvalue=True, offvalue=False)   
        shuffle_button.pack(pady=10)

        prev_test_frame = tk.Frame(init_frame_var)
        prev_test_frame.pack(pady=10, anchor="center", fill="x")
        prev_button = tk.Radiobutton(prev_test_frame, text="Previous Test", command=self.prev_test.load_previous_test)
        prev_button.pack(side="left", padx=10)
        self.prev_test_path = tk.Label(prev_test_frame, text="Select the previous test file", wraplength=400, justify="left")
        self.prev_test_path.pack(side="left", padx=10)
        cancel_prev_button = tk.Button(prev_test_frame, text="Cancel", command=self.prev_test.off_pflag)
        cancel_prev_button.pack(side="left", padx=10)
        
        start_button = tk.Button(init_frame_var, text="Iniciar Test", command=self.init.start_test)
        start_button.pack(pady=10)

    def test_frame(self):
        self.add_frame("test_frame")
        f = self.get_frame("test_frame")

        #Método para que la ventana sea scrollable
        self.test_canvas = tk.Canvas(f)
        self.test_canvas.pack(side="left", fill="both", expand=True)
        self.current_canvas = self.test_canvas
        y_scrollbar = ttk.Scrollbar(f, orient="vertical", command=self.test_canvas.yview)
        y_scrollbar.pack(side="right", fill="y")
        self.test_canvas.configure(yscrollcommand=y_scrollbar.set)
        self.test_canvas.bind("<Configure>", lambda e: self.test_canvas.configure(scrollregion=self.test_canvas.bbox("all")))
        self.test_canvas.bind_all("<MouseWheel>", lambda event: self.test_canvas.yview_scroll(int(-1*(event.delta/120)), "units"))

        self.test_frame_var = tk.Frame(self.test_canvas)
        self.test_canvas.create_window((0, 0), window=self.test_frame_var, anchor="nw")
        self.current_frame = self.test_frame_var

        self.question_image = tk.Label(self.test_frame_var)
        self.question_image.pack(pady=10)

        self.question_label = tk.Label(self.test_frame_var, text="Pregunta", wraplength=400, justify="left")
        self.question_label.pack(pady=10)
        
        self.options_var = tk.StringVar()
        self.options_buttons = []
        for i in self.qfile.opciones_preguntas:
            button = tk.Radiobutton(self.test_frame_var, text="", variable=self.options_var, value=i)
            button.pack(anchor="w")
            self.options_buttons.append(button)

        button_frame = tk.Frame(self.test_frame_var)
        button_frame.pack(pady=10, anchor="center", fill="x")

        clean_button = tk.Button(button_frame, text="Borrar", command=self.questionaire.reset_selection)
        clean_button.pack(side="left", padx=5)

        next_button = tk.Button(button_frame, text="Siguiente", command=self.questionaire.next_question)
        next_button.pack(side="left", padx=5)

        finish_button = tk.Button(button_frame, text="Terminar", command=self.questionaire.end_test)
        finish_button.pack(side="left", padx=5)
        bottom_frame = tk.Frame(self.test_frame_var)
        bottom_frame.pack(pady=10, anchor="center", fill="x")
        if self.prev_test.flag_pmode:
            self.status_label = tk.Label(bottom_frame, text=f"Estado: {self.questionaire.correcto} correctos, {self.questionaire.fallado} fallados, {self.questionaire.blanco} en blanco")
        else:
            self.status_label = tk.Label(bottom_frame, text="Estado: 0 correctos, 0 fallados, 0 en blanco")
        self.status_label.pack(side="left", padx=10)
        self.question_id_label = tk.Label(bottom_frame, text=f"Respondidas: {len(self.qfile.preguntas_realizadas)}/{self.qfile.num_preguntas}")
        self.question_id_label.pack(side="left", padx=10)
        self.show_frame("test_frame")


    def study_frame(self):
        self.add_frame("study_frame")
        f = self.get_frame("study_frame")

        #Método para que la ventana sea scrollable
        self.study_canvas = tk.Canvas(f)
        self.study_canvas.pack(side="left", fill="both", expand=True)
        self.current_canvas = self.study_canvas
        y_scrollbar = ttk.Scrollbar(f, orient="vertical", command=self.study_canvas.yview)
        y_scrollbar.pack(side="right", fill="y")
        self.study_canvas.configure(yscrollcommand=y_scrollbar.set)
        self.study_canvas.bind("<Configure>", lambda e: self.study_canvas.configure(scrollregion=self.study_canvas.bbox("all")))
        self.study_canvas.bind_all("<MouseWheel>", lambda event: self.study_canvas.yview_scroll(int(-1*(event.delta/120)), "units"))


        self.study_frame_var = tk.Frame(self.study_canvas)
        self.study_canvas.create_window((0, 0), window=self.study_frame_var, anchor="nw")
        self.current_frame = self.study_frame_var

        self.study_question_image = tk.Label(self.study_frame_var)
        self.study_question_image.pack(pady=10)

        self.study_question_label = tk.Label(self.study_frame_var, text="Pregunta", wraplength=400, justify="left")
        self.study_question_label.pack(pady=10)
        
        self.study_options_var = tk.StringVar()
        self.study_options_buttons = []
        for i in self.qfile.opciones_preguntas:
            button = tk.Radiobutton(self.study_frame_var, text="", variable=self.study_options_var, value=i)
            button.pack(anchor="w")
            self.study_options_buttons.append(button)

        button_frame = tk.Frame(self.study_frame_var)
        button_frame.pack(pady=10, anchor="center", fill="x")

        clean_button = tk.Button(button_frame, text="Borrar", command=self.smode.smode_reset_selection)
        clean_button.pack(side="left", padx=5)

        self.study_previous_button = tk.Button(button_frame, text="Previous", command=self.smode.smode_previous_question, state="disabled")
        self.study_previous_button.pack(side="left", padx=5)
        

        self.study_next_button = tk.Button(button_frame, text="Validar", command=self.smode.smode_next_question)
        self.study_next_button.pack(side="left", padx=5)

        finish_button = tk.Button(button_frame, text="Terminar", command=self.smode.smode_end_test)
        finish_button.pack(side="left", padx=5)

        study_percentage_frame = tk.Frame(self.study_frame_var)
        study_percentage_frame.pack(pady=10, anchor="center", fill="x")
        #Objetivo: Marcar el porcentaje de preguntas correctas e incorrectas mientras se va realizando el test
        self.study_percentage_correct_label = tk.Label(study_percentage_frame, text="--%", bg="green")
        self.study_percentage_correct_label.pack(side="left", padx=10)
        self.study_percentage_incorrect_label = tk.Label(study_percentage_frame, text="--%", bg="red")
        self.study_percentage_incorrect_label.pack(side="left", padx=10)
        self.study_question_id_label = tk.Label(study_percentage_frame, text=f"Respondidas: {len(self.qfile.preguntas_realizadas)}/{self.qfile.num_preguntas}")
        self.study_question_id_label.pack(side="left", padx=10)

        self.show_frame("study_frame")
    
    def adjust_canvas(self, selected_canvas, selected_frame):
        selected_canvas.yview_moveto(0)
        selected_canvas.after(100,self.update_scrollregion, selected_canvas, selected_frame)

    def update_scrollregion(self, selected_canvas, selected_frame):
        selected_frame.update_idletasks()
        selected_canvas.configure(scrollregion=selected_canvas.bbox("all"))

    def check_box(self, event):
        self.qfile.test_title = self.combo.get()
        self.qfile.set_num_preguntas()   