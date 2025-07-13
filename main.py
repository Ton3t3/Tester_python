import json
import os
import datetime
import tkinter as tk
from tkinter import messagebox, filedialog
from random import choice
import sys

from classes.questionaire_class import Questionaire
from classes.shuffle_class import Shuffle
from classes.Qfile_class import Question_file
from classes.excel_to_json_class import ExccelToJson
from classes.previous_test_class import PreviousTest
from classes.study_mode_class import SMode
from classes.frame_manager_class import FrameManager
    
class Init:
    def __init__(self, root):
        self.root = root
        self.root.title("Test de Preguntas")
        # self.root_path = os.path.dirname(sys.executable)           #PARA .EXE!!!!
        self.root_path = os.path.dirname(os.path.abspath(__file__))       #PARA .PY!!!!!

    def start_test(self):
        if study_mode.flag_smode:
            frame_manager.study_frame()
            self.root.title(f"Test de Preguntas [Test: {question_file.nombre_fichero_preguntas[:-5]}] [STUDY MODE: ON] [Test name: {question_file.test_title}]")
        else:
            frame_manager.test_frame()
            self.root.title(f"Test de Preguntas [Test: {question_file.nombre_fichero_preguntas[:-5]}] [Shuffle: {"ON" if int(shuffle.flag_shuffle) == 1 else "OFF"}] [Test name: {question_file.test_title}]")
        question_file.display_question()



if __name__ == "__main__":
    root = tk.Tk()

    initializer = Init(root)
    shuffle = Shuffle()
    excel_to_json = ExccelToJson()
    question_file = Question_file(initializer, None, shuffle, None, None, None, excel_to_json)
    questionaire = Questionaire(question_file, shuffle, None, initializer, root, None)
    question_file.questionaire = questionaire
    study_mode = SMode(question_file, questionaire, None, root)
    # widget = Widget(root, questionaire, question_file, shuffle, initializer, study_mode, None)
    # study_mode.widget = widget
    question_file.smode = study_mode
    prev_test = PreviousTest(initializer, questionaire, shuffle, question_file, None)
    questionaire.prev_test = prev_test
    question_file.prev_test = prev_test
    frame_manager = FrameManager(root, questionaire, question_file, shuffle, study_mode, prev_test, initializer)
    prev_test.frame_manager = frame_manager
    question_file.frame_manager = frame_manager
    # widget.frame_manager = frame_manager
    questionaire.frame_manager = frame_manager
    study_mode.frame_manager = frame_manager

    frame_manager.init_frame()

    root.mainloop()
