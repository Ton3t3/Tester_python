import json
import os
import datetime
import tkinter as tk
from tkinter import messagebox, filedialog, Frame
from random import choice
import random
import time


class FrameManager:
    def __init__(self, root, questionaire, qfile, shuffle, smode, prev_test, init):
        self.root = root
        self.questionaire = questionaire
        self.qfile = qfile 
        self.shuffle = shuffle
        self.smode = smode
        self.prev_test = prev_test
        self.init = init

        self.frames = {}
        self.current_frame = None
        self.question_label = None
        self.status_label = None
        self.options_buttons = None
        self.options_var = None

        self.study_question_label = None
        self.study_status_label = None
        self.study_options_buttons = None
        self.study_options_var = None
        self.study_next_button = None
        self.study_previous_button = None

    def add_frame(self, name:str):
        frame = Frame(self.root)
        self.frames[name] = frame
        if self.current_frame is None:
            self.current_frame = frame
            frame.pack(fill="both", expand=True)
    
    def get_frame(self, name:str):
        return self.frames.get(name)

    def show_frame(self, name:str):
        if name in self.frames:
            if self.current_frame is not None:
                self.current_frame.pack_forget()
            self.current_frame = self.frames[name]
            self.current_frame.pack(fill="both", expand=True)


    def init_frame(self):
        self.add_frame("init_frame")
        f1 = self.get_frame("init_frame")
        
        question_file_frame = tk.Frame(f1)
        question_file_frame.pack(pady=10, anchor="center", fill="x")
        question_file_button = tk.Radiobutton(question_file_frame, text="Seleccionar fichero de preguntas", command=self.qfile.load_question_file)
        question_file_button.pack(side="left", padx=10)
        self.question_file_path = tk.Label(question_file_frame, text="Seleccionar fichero de preguntas", wraplength=400, justify="left")
        self.question_file_path.pack(side="left", padx=10)

        studio_button = tk.Checkbutton(f1, text="Modo Estudio", command=lambda:self.smode.turn_sflag(), onvalue=True, offvalue=False)
        studio_button.pack(pady=10)

        shuffle_button = tk.Checkbutton(f1, text="Modo Shuffle", command=lambda:self.shuffle.turn_shuffle_flag(), onvalue=True, offvalue=False)   
        shuffle_button.pack(pady=10)

        prev_test_frame = tk.Frame(f1)
        prev_test_frame.pack(pady=10, anchor="center", fill="x")
        prev_button = tk.Radiobutton(prev_test_frame, text="Previous Test", command=self.prev_test.load_previous_test)
        prev_button.pack(side="left", padx=10)
        self.prev_test_path = tk.Label(prev_test_frame, text="Select the previous test file", wraplength=400, justify="left")
        self.prev_test_path.pack(side="left", padx=10)
        cancel_prev_button = tk.Button(prev_test_frame, text="Cancel", command=self.prev_test.off_pflag)
        cancel_prev_button.pack(side="left", padx=10)
        
        start_button = tk.Button(f1, text="Iniciar Test", command=self.init.start_test)
        start_button.pack(pady=10)

    def test_frame(self):
        self.add_frame("test_frame")
        f = self.get_frame("test_frame")

        self.question_label = tk.Label(f, text="Pregunta", wraplength=400, justify="left")
        self.question_label.pack(pady=10)
        
        self.options_var = tk.StringVar()
        self.options_buttons = []
        for i in self.qfile.opciones_preguntas:
            button = tk.Radiobutton(f, text="", variable=self.options_var, value=i)
            button.pack(anchor="w")
            self.options_buttons.append(button)

        button_frame = tk.Frame(f)
        button_frame.pack(pady=10, anchor="center", fill="x")

        clean_button = tk.Button(button_frame, text="Borrar", command=self.questionaire.reset_selection)
        clean_button.pack(side="left", padx=5)

        next_button = tk.Button(button_frame, text="Siguiente", command=self.questionaire.next_question)
        next_button.pack(side="left", padx=5)

        finish_button = tk.Button(button_frame, text="Terminar", command=self.questionaire.end_test)
        finish_button.pack(side="left", padx=5)
        if self.prev_test.flag_pmode:
            self.status_label = tk.Label(f, text=f"Estado: {self.questionaire.correcto} correctos, {self.questionaire.fallado} fallados, {self.questionaire.blanco} en blanco")
        else:
            self.status_label = tk.Label(f, text="Estado: 0 correctos, 0 fallados, 0 en blanco")
        self.status_label.pack(pady=10)
        self.show_frame("test_frame")


    def study_frame(self):
        self.add_frame("study_frame")
        f = self.get_frame("study_frame")

        self.study_question_label = tk.Label(f, text="Pregunta", wraplength=400, justify="left")
        self.study_question_label.pack(pady=10)
        
        self.study_options_var = tk.StringVar()
        self.study_options_buttons = []
        for i in self.qfile.opciones_preguntas:
            button = tk.Radiobutton(f, text="", variable=self.study_options_var, value=i)
            button.pack(anchor="w")
            self.study_options_buttons.append(button)

        button_frame = tk.Frame(f)
        button_frame.pack(pady=10, anchor="center", fill="x")

        clean_button = tk.Button(button_frame, text="Borrar", command=self.smode.smode_reset_selection)
        clean_button.pack(side="left", padx=5)

        self.study_previous_button = tk.Button(button_frame, text="Previous", command=self.smode.smode_previous_question)
        self.study_previous_button.pack(side="left", padx=5)
        

        self.study_next_button = tk.Button(button_frame, text="Validar", command=self.smode.smode_next_question)
        self.study_next_button.pack(side="left", padx=5)

        finish_button = tk.Button(button_frame, text="Terminar", command=self.smode.smode_end_test)
        finish_button.pack(side="left", padx=5)

        self.study_status_label = tk.Label(f, text="MODO ESTUDIO")
        self.study_status_label.pack(pady=10)

        self.show_frame("study_frame")