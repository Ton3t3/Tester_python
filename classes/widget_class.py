import json
import os
import datetime
import tkinter as tk
from tkinter import messagebox, filedialog
from random import choice


class Widget:
    def __init__(self, root, questionaire, qfile, shuffle, init, smode):
        self.questionaire = questionaire
        self.root = root
        self.qfile = qfile
        self.shuffle = shuffle
        self.init = init
        self.smode = smode

        self.question_label = tk.Label(self.root, text="Pregunta", wraplength=400, justify="left")
        self.question_label.pack(pady=10)
        
        self.options_var = tk.StringVar()
        self.options_buttons = []
        for i in self.qfile.opciones_preguntas:
            button = tk.Radiobutton(self.root, text="", variable=self.options_var, value=i)
            button.pack(anchor="w")
            self.options_buttons.append(button)

        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10, anchor="center", fill="x")

        self.clean_button = tk.Button(button_frame, text="Borrar", command=self.reset_selection)
        self.clean_button.pack(side="left", padx=5)

        self.previous_button = tk.Button(button_frame, text="Previous", state="disabled", command=self.smode.smode_previous_question)
        # self.previous_button.pack(side="left", padx=5)
        self.previous_button.pack_forget()
        

        self.next_button = tk.Button(button_frame, text="Siguiente", command=self.next_question)
        self.next_button.pack(side="left", padx=5)

        self.finish_button = tk.Button(button_frame, text="Terminar", command=self.end_test)
        self.finish_button.pack(side="left", padx=5)


        self.status_label = tk.Label(self.root, text="Estado: 0 correctos, 0 fallados, 0 en blanco")
        self.status_label.pack(pady=10)

    def reset_selection(self):
        self.options_var.set("")

    def next_question(self):
        respuesta = self.options_var.get()
        pregunta = self.qfile.data['emp_details'][self.qfile.current_question]

        self.questionaire.results_manager(respuesta, pregunta)

        self.qfile.preguntas_realizadas.append(self.qfile.current_question)
        self.status_label.config(text=f"Estado: {self.questionaire.correcto} correctos, {self.questionaire.fallado} fallados, {self.questionaire.blanco} en blanco")

        self.qfile.display_question()


    def end_test(self):
        now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        if self.qfile.nombre_test_anterior == "":
            save_path = os.path.join(self.init.root_path, "TESTS ANTERIORES", f"Test_{self.qfile.nombre_fichero_preguntas[:-5]}_{now}.txt")
        else:
            save_path = os.path.join(self.init.root_path, "TESTS ANTERIORES", f"CONT_{self.qfile.nombre_test_anterior}")
        os.makedirs(os.path.dirname(save_path), exist_ok=True)

        with open(save_path, "w") as f:
            f.write(f"FINAL DEL TEST {datetime.datetime.now().isoformat()}\n")
            f.write(f"\nShuffle ON(1)/OFF(0): {int(self.shuffle.flag_shuffle)}")
            f.write(f"\nTotal de pregunta realizadas: {len(self.qfile.preguntas_realizadas)}")
            f.write(f"\n{self.qfile.preguntas_realizadas}")
            f.write(f"\n{[self.questionaire.correcto, self.questionaire.blanco, self.questionaire.fallado]}")

           
            if self.qfile.nombre_test_anterior != "":
                f.write(f"\n\nAciertos_TOT: {self.questionaire.correcto}\t\tLibres_TOT: {self.questionaire.blanco}\t\tFallos_TOT: {self.questionaire.fallado}")
            else:
                f.write(f"\n\n")
            f.write(f"\n\nAciertos: {self.questionaire.correcto_actual}\t\tLibres: {self.questionaire.blanco_actual}\t\tFallos: {self.questionaire.fallado_actual} \ten las preguntas:\n")

            self.questionaire.id_fallado = sorted(self.questionaire.id_fallado)
            self.questionaire.contestado = sorted(self.questionaire.contestado)
            if self.shuffle.flag_shuffle:
                self.shuffle.solucion_mezclada_lista = sorted(self.shuffle.solucion_mezclada_lista)
            id = 0
            for i in self.questionaire.id_fallado:
                f.write(f"\nTest {self.qfile.data['emp_details'][i]['test']}: {self.qfile.data['emp_details'][i]['question']}")
                #Ya no se corresponde con la letra de la respuesta correcta del JSON!!
                opcion_buena_JSON = self.qfile.data['emp_details'][i]['solution']
                if self.shuffle.flag_shuffle:   #SHUFFLE MODE
                    f.write(f"\n\tContestado: {self.questionaire.contestado[id][1]}\tRespuesta correcta: {self.shuffle.solucion_mezclada_lista[id][1]} ({self.qfile.data['emp_details'][i]["options"][0][opcion_buena_JSON]})")
                else:                   #NORMAL MODE
                    f.write(f"\n\tContestado: {self.questionaire.contestado[id][1]}\tRespuesta correcta: {opcion_buena_JSON} ({self.qfile.data['emp_details'][i]["options"][0][opcion_buena_JSON]})")
                id += 1
            # En caso de que haya un test anterior, se añade su contenido al final del fichero
            if self.qfile.nombre_test_anterior != "":
                f.write(f"\n\n")
                for i in range(10,len(self.qfile.lineas)):
                    f.write(f"{self.qfile.lineas[i]}")
        messagebox.showinfo("Finalizado", f"El test ha terminado. Resultados guardados en {save_path}")
        self.root.quit()