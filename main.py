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
    
class Init:
    def __init__(self, root):
        self.root = root
        self.root.title("Test de Preguntas")
        self.root_path = os.path.dirname(sys.executable)           #PARA .EXE!!!!
        # self.root_path = os.path.dirname(os.path.abspath(__file__))       #PARA .PY!!!!!


if __name__ == "__main__":
    root = tk.Tk()

    initializer = Init(root)
    shuffle = Shuffle()
    question_file = Question_file(initializer, None, shuffle)
    questionaire = Questionaire(question_file)
    widget = Widget(root, questionaire, question_file, shuffle, initializer)
    question_file.widget = widget
    prev_test = PreviousTest(initializer, questionaire, shuffle, widget, question_file)

    prev_test.load_previous_test()
    question_file.display_question()

    root.mainloop()