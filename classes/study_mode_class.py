import json
import os
import datetime
import tkinter as tk
from tkinter import messagebox, filedialog
from random import choice
import random
import time


class SMode:
    def __init__(self, qfile, questionaire, frame_manager, root):
        self.qfile = qfile
        self.root = root
        self.frame_manager = frame_manager
        self.questionaire = questionaire
        
        self.flag_smode = False
        self.flag_last_question = True
        self.blinked = False
        self.previous_question_buffer = []
        self.actual_previous_id = 0
        self.actual_previous_bpos = 0
        self.correct_percentage = 0
        self.incorrect_percentage = 0
        self.correct_questions = 0
        self.incorrect_questions = 0
        self.smode_retrieve_results = False
        
    
    def turn_sflag(self):
        self.flag_smode = not self.flag_smode

    def turn_results_flag(self):
        self.smode_retrieve_results = not self.smode_retrieve_results
    # def study_mode_activation(self):

    #     self.widget.clean_button.pack_forget()
    #     self.widget.next_button.pack_forget()
    #     self.widget.finish_button.pack_forget()

    #     self.widget.clean_button.pack(side="left", padx=5)
    #     self.widget.previous_button.pack(side="left", padx=5)
    #     self.widget.next_button.pack(side="left", padx=5)
    #     self.widget.finish_button.pack(side="left", padx=5)

    #     self.widget.next_button.config(command=self.smode_next_question, text="Validar")
    #     self.widget.finish_button.config(command=self.smode_end_test)
    #     self.widget.status_label.config(text="MODO ESTUDIO")

    def smode_reset_selection(self):
        self.frame_manager.study_options_var.set("")

    def smode_previous_question(self):
        # print("prev")
        if self.flag_last_question:
            self.flag_last_question = False
            self.previous_question_buffer = self.qfile.preguntas_realizadas.copy()
            self.previous_question_buffer.append(self.qfile.current_question)
            self.frame_manager.study_next_button.config(command=self.smode_next_question, text="Siguiente")
            self.actual_previous_id = self.previous_question_buffer[-2]
            self.actual_previous_bpos = len(self.previous_question_buffer)-2
        else:
            self.actual_previous_bpos -= 1
            self.actual_previous_id = self.previous_question_buffer[self.actual_previous_bpos]

        if self.actual_previous_bpos == 0:
            self.frame_manager.study_previous_button.config(state="disabled")       
        self.smode_display_question()


    def smode_next_question(self):
        """
        · En caso de ser la úlitma respuesta contestada (botón validar), tendrá que mostrar si la opción marcada es correcta, y avanzará
            a una nueva pregunta.

        · En el caso de haber seleccionado el botón de atrás previamente, se tendrá que calcular si la pregunta siguiente es la última por 
            resolver (boton validar), o si todavía quedan preguntas respondidas previamente (botón siguiente).
        """

        if self.flag_last_question:
            respuesta = self.frame_manager.study_options_var.get()
            pregunta = self.qfile.data['emp_details'][self.qfile.current_question] 
            if respuesta == pregunta['solution']:
                self.blink(self.frame_manager.study_options_buttons[self.letra_a_num(respuesta)], "#64ff33")
                self.correct_questions += 1
            else:
                self.blink(self.frame_manager.study_options_buttons[self.letra_a_num(respuesta)], "#C70039")
                self.incorrect_questions += 1

            self.questionaire.results_manager(respuesta, pregunta)

            self.qfile.preguntas_realizadas.append(self.qfile.current_question)
            self.correct_percentage = (self.correct_questions / len(self.qfile.preguntas_realizadas)) * 100
            self.incorrect_percentage = (self.incorrect_questions / len(self.qfile.preguntas_realizadas)) * 100
            self.frame_manager.study_percentage_correct_label.config(text=f"{self.correct_percentage:.2f}%")
            self.frame_manager.study_percentage_incorrect_label.config(text=f"{self.incorrect_percentage:.2f}%")
            if len(self.qfile.preguntas_realizadas) == 1:
                self.frame_manager.study_previous_button.config(state="normal")
            self.qfile.display_question()
        else:
            if self.actual_previous_id == self.previous_question_buffer[-2]:
                self.frame_manager.study_next_button.config(command=self.smode_next_question, text="Validar")
                self.flag_last_question = True
                self.actual_previous_bpos += 1
                self.actual_previous_id = self.previous_question_buffer[self.actual_previous_bpos]
            else: 
                self.actual_previous_bpos += 1
                self.actual_previous_id = self.previous_question_buffer[self.actual_previous_bpos]

            if self.actual_previous_bpos == 1:
                self.frame_manager.study_previous_button.config(state="normal")   
            self.smode_display_question()
  

    def smode_display_question(self):
        if len(self.qfile.preguntas_realizadas) >= self.qfile.num_preguntas:
            self.smode_end_test()
            return
        
        current_question = self.previous_question_buffer[self.actual_previous_bpos]
        pregunta = self.qfile.data['emp_details'][current_question]
        
        self.frame_manager.study_question_label.config(text=pregunta["question"])
        opciones = pregunta["options"][0]
        
        self.qfile.display_image(pregunta)

        for i, key in enumerate(self.qfile.opciones_preguntas):
            self.frame_manager.study_options_buttons[i].config(text=f"{key}: {opciones[key]}")
        
            if not(self.flag_last_question):
                """Hay que indicar la solución!!"""
                if key == pregunta['solution']:
                    self.frame_manager.study_options_buttons[i].config(foreground="#64ff33")
                else:
                    self.frame_manager.study_options_buttons[i].config(foreground="#C70039")
            else:
                self.frame_manager.study_options_buttons[i].config(foreground="#000000")
                # self.frame_manager.study_options_buttons[i].config(foreground="#000000")

        self.frame_manager.adjust_canvas(self.frame_manager.current_canvas, self.frame_manager.current_frame)
        self.frame_manager.study_options_var.set("")

        
    def smode_end_test(self):
        if self.smode_retrieve_results:
            self.questionaire.end_test()
        else:
            messagebox.showinfo("Finalizado", f"El test ha terminado")
            self.root.quit()

    def blink(self, button, color_id):
        if self.blinked:
            button.config(background="SystemButtonFace")
            self.blinked = False
        else:
            button.config(background=color_id)
            self.blinked = True
            self.root.after(150, self.blink, button, color_id)  # Toggle color every 250ms

    def letra_a_num(self, respuesta):
        for i, key in enumerate(self.qfile.opciones_preguntas):
            if respuesta == key:
                return i
        return len(self.qfile.opciones_preguntas)-1

    