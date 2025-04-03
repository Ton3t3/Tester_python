import json
import os
import datetime
import tkinter as tk
from tkinter import messagebox, filedialog
from random import choice
import sys

from classes.questionaire_class import Questionaire
from classes.widget_class import Widget
from classes.shuffle_class import Shuffle
from classes.Qfile_class import Question_file
from classes.previous_test_class import PreviousTest
from classes.study_mode_class import SMode
    
class Init:
    def __init__(self, root):
        self.root = root
        self.root.title("Test de Preguntas")
        # self.root_path = os.path.dirname(sys.executable)           #PARA .EXE!!!!
        self.root_path = os.path.dirname(os.path.abspath(__file__))       #PARA .PY!!!!!


if __name__ == "__main__":
    root = tk.Tk()

    initializer = Init(root)
    shuffle = Shuffle()
    question_file = Question_file(initializer, None, shuffle, None)
    questionaire = Questionaire(question_file, shuffle)
    study_mode = SMode(None, question_file, root)
    widget = Widget(root, questionaire, question_file, shuffle, initializer, study_mode)
    study_mode.widget = widget
    question_file.widget = widget
    question_file.smode = study_mode
    prev_test = PreviousTest(initializer, questionaire, shuffle, widget, question_file)
    

    study_mode.flag_smode = bool(int(messagebox.askyesno("LMode", "¿Desea activar el modo estudio?")))
    if study_mode.flag_smode:  
        study_mode.study_mode_activation()
    else:
        prev_test.load_previous_test()

    question_file.display_question()

    root.mainloop()