import json
import os
import datetime
import tkinter as tk
from tkinter import messagebox, filedialog
from random import choice

class Questionaire:
    def __init__(self, qfile, shuffle, frame_manager, init, root):
        self.qfile = qfile
        self.shuffle = shuffle
        self.frame_manager = frame_manager
        self.init = init
        self.root = root

        #% Variables para referenciar los resultados de las preguntas de test anteriores     
        self.correcto = 0
        self.fallado = 0
        self.blanco = 0

        #% Variables para referenciar los resultados de las preguntas de test actuales
        self.correcto_actual = 0
        self.fallado_actual = 0
        self.blanco_actual = 0

        #% Listas para guardar las preguntas falladas/blanco y la respuesta dada
        self.id_fallado = []
        self.contestado = []
    
    def reset_selection(self):
        self.frame_manager.options_var.set("")

    def next_question(self):
        respuesta = self.frame_manager.options_var.get()
        pregunta = self.qfile.data['emp_details'][self.qfile.current_question]

        self.results_manager(respuesta, pregunta)

        self.qfile.preguntas_realizadas.append(self.qfile.current_question)
        self.frame_manager.status_label.config(text=f"Estado: {self.correcto} correctos, {self.fallado} fallados, {self.blanco} en blanco")

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
            f.write(f"\n{[self.correcto, self.blanco, self.fallado]}")

           
            if self.qfile.nombre_test_anterior != "":
                f.write(f"\n\nAciertos_TOT: {self.correcto}\t\tLibres_TOT: {self.blanco}\t\tFallos_TOT: {self.fallado}")
            else:
                f.write(f"\n\n")
            f.write(f"\n\nAciertos: {self.correcto_actual}\t\tLibres: {self.blanco_actual}\t\tFallos: {self.fallado_actual} \ten las preguntas:\n")

            self.id_fallado = sorted(self.id_fallado)
            self.contestado = sorted(self.contestado)
            if self.shuffle.flag_shuffle:
                self.shuffle.solucion_mezclada_lista = sorted(self.shuffle.solucion_mezclada_lista)
            id = 0
            for i in self.id_fallado:
                f.write(f"\nTest {self.qfile.data['emp_details'][i]['test']}: {self.qfile.data['emp_details'][i]['question']}")
                #Ya no se corresponde con la letra de la respuesta correcta del JSON!!
                opcion_buena_JSON = self.qfile.data['emp_details'][i]['solution']
                if self.shuffle.flag_shuffle:   #SHUFFLE MODE
                    f.write(f"\n\tContestado: {self.contestado[id][1]}\tRespuesta correcta: {self.shuffle.solucion_mezclada_lista[id][1]} ({self.qfile.data['emp_details'][i]["options"][0][opcion_buena_JSON]})")
                else:                   #NORMAL MODE
                    f.write(f"\n\tContestado: {self.contestado[id][1]}\tRespuesta correcta: {opcion_buena_JSON} ({self.qfile.data['emp_details'][i]["options"][0][opcion_buena_JSON]})")
                id += 1
            # En caso de que haya un test anterior, se añade su contenido al final del fichero
            if self.qfile.nombre_test_anterior != "":
                f.write(f"\n\n")
                for i in range(10,len(self.qfile.lineas)):
                    f.write(f"{self.qfile.lineas[i]}")
        messagebox.showinfo("Finalizado", f"El test ha terminado. Resultados guardados en {save_path}")
        self.root.quit()



    
    def results_manager(self, respuesta, pregunta):
        if self.shuffle.flag_shuffle == False:                  #NORMAL MODE
            solucion_correcta = pregunta["solution"]
        else:                                           #SUFFLE MODE
            solucion_correcta = self.shuffle.solucion_mezclada

        if respuesta == solucion_correcta:
            self.correcto += 1
            self.correcto_actual += 1
        elif respuesta == "":
            self.blanco += 1
            self.blanco_actual += 1
            self.id_fallado += [self.qfile.current_question]
            self.contestado += [(self.qfile.current_question,"BLANCO")]
            if self.shuffle.flag_shuffle:
                self.shuffle.solucion_mezclada_lista += [(self.qfile.current_question, self.shuffle.solucion_mezclada)]
        else:
            self.fallado += 1
            self.fallado_actual += 1
            self.id_fallado += [self.qfile.current_question]
            self.contestado += [(self.qfile.current_question,respuesta)]
            if self.shuffle.flag_shuffle:
                self.shuffle.solucion_mezclada_lista += [(self.qfile.current_question, self.shuffle.solucion_mezclada)]