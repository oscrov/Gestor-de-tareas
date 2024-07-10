import pickle
import tkinter as tk
from tkinter import messagebox, simpledialog

class Tarea:
    def __init__(self, descripcion, prioridad):
        self.descripcion = descripcion
        self.prioridad = prioridad

    def __repr__(self):
        return f"{self.descripcion} ({self.prioridad})"

class GestorTareas:
    def __init__(self):
        self.pila_alta = []
        self.cola_media = []
        self.cola_baja = []

    def agregar_tarea(self, descripcion, prioridad):
        tarea = Tarea(descripcion, prioridad)
        if prioridad == 'alta':
            self.pila_alta.append(tarea)
        elif prioridad == 'media':
            self.cola_media.append(tarea)
        elif prioridad == 'baja':
            self.cola_baja.append(tarea)
        else:
            print("Prioridad inválida. Use 'alta', 'media' o 'baja'.")

    def ver_tareas(self):
        tareas = {
            'alta': list(reversed(self.pila_alta)),
            'media': self.cola_media,
            'baja': self.cola_baja
        }
        return tareas

    def completar_tarea(self, prioridad):
        if prioridad == 'alta' and self.pila_alta:
            return self.pila_alta.pop()
        elif prioridad == 'media' and self.cola_media:
            return self.cola_media.pop(0)
        elif prioridad == 'baja' and self.cola_baja:
            return self.cola_baja.pop(0)
        else:
            return None

    def guardar_tareas(self, archivo):
        with open(archivo, 'wb') as f:
            pickle.dump((self.pila_alta, self.cola_media, self.cola_baja), f)

    def cargar_tareas(self, archivo):
        try:
            with open(archivo, 'rb') as f:
                self.pila_alta, self.cola_media, self.cola_baja = pickle.load(f)
        except FileNotFoundError:
            print("Archivo no encontrado. Comenzando con tareas vacías.")

class GestorTareasApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestor de Tareas")
        self.gestor = GestorTareas()
        self.archivo_tareas = 'tareas.pkl'
        self.gestor.cargar_tareas(self.archivo_tareas)

        self.frame = tk.Frame(root)
        self.frame.pack(pady=20)

        self.ver_tareas_button = tk.Button(self.frame, text="Ver Tareas", command=self.ver_tareas)
        self.ver_tareas_button.grid(row=0, column=0, padx=10)

        self.agregar_tarea_button = tk.Button(self.frame, text="Agregar Tarea", command=self.agregar_tarea)
        self.agregar_tarea_button.grid(row=0, column=1, padx=10)

        self.completar_tarea_button = tk.Button(self.frame, text="Completar Tarea", command=self.completar_tarea)
        self.completar_tarea_button.grid(row=0, column=2, padx=10)

        self.guardar_tareas_button = tk.Button(self.frame, text="Guardar Tareas", command=self.guardar_tareas)
        self.guardar_tareas_button.grid(row=0, column=3, padx=10)

        self.cargar_tareas_button = tk.Button(self.frame, text="Cargar Tareas", command=self.cargar_tareas)
        self.cargar_tareas_button.grid(row=0, column=4, padx=10)

        self.tareas_text = tk.Text(root, width=80, height=20)
        self.tareas_text.pack(pady=20)

    def ver_tareas(self):
        tareas = self.gestor.ver_tareas()
        self.tareas_text.delete(1.0, tk.END)
        self.tareas_text.insert(tk.END, "Tareas de alta prioridad:\n")
        for tarea in tareas['alta']:
            self.tareas_text.insert(tk.END, f"{tarea}\n")
        self.tareas_text.insert(tk.END, "\nTareas de media prioridad:\n")
        for tarea in tareas['media']:
            self.tareas_text.insert(tk.END, f"{tarea}\n")
        self.tareas_text.insert(tk.END, "\nTareas de baja prioridad:\n")
        for tarea in tareas['baja']:
            self.tareas_text.insert(tk.END, f"{tarea}\n")

    def agregar_tarea(self):
        descripcion = simpledialog.askstring("Agregar Tarea", "Descripción de la tarea:")
        prioridad = simpledialog.askstring("Agregar Tarea", "Prioridad (alta, media, baja):")
        if descripcion and prioridad:
            self.gestor.agregar_tarea(descripcion, prioridad)
            self.ver_tareas()

    def completar_tarea(self):
        prioridad = simpledialog.askstring("Completar Tarea", "Prioridad de la tarea a completar (alta, media, baja):")
        if prioridad:
            tarea = self.gestor.completar_tarea(prioridad)
            if tarea:
                messagebox.showinfo("Completar Tarea", f"Tarea completada: {tarea}")
            else:
                messagebox.showwarning("Completar Tarea", "No hay tareas en esta prioridad o prioridad inválida.")
            self.ver_tareas()

    def guardar_tareas(self):
        self.gestor.guardar_tareas(self.archivo_tareas)
        messagebox.showinfo("Guardar Tareas", "Tareas guardadas.")

    def cargar_tareas(self):
        self.gestor.cargar_tareas(self.archivo_tareas)
        self.ver_tareas()
        messagebox.showinfo("Cargar Tareas", "Tareas cargadas.")

if __name__ == "__main__":
    root = tk.Tk()
    app = GestorTareasApp(root)
    root.mainloop()
