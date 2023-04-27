import tkinter as tk

# Función que se encarga de configurar la scrollbar
def scroll_config(*args):
    canvas.configure(scrollregion=canvas.bbox("all"), width=500, height=500)

# Crear la ventana principal
root = tk.Tk()

# Crear el contenedor
container = tk.Frame(root)
container.pack()

# Crear el objeto Scrollbar y asociarlo con el contenedor
scrollbar = tk.Scrollbar(container)
scrollbar.pack(side="right", fill="y")

# Crear el objeto Canvas para contener el Label y asociarlo con el contenedor y la scrollbar
canvas = tk.Canvas(container, yscrollcommand=scrollbar.set)
canvas.pack(side="left", fill="both", expand=True)

# Configurar la scrollbar para que funcione correctamente
scrollbar.config(command=canvas.yview)
canvas.bind("<Configure>", scroll_config)

# Crear el Label con el texto
label_text = "Este es un texto muy largo que se va a mostrar dentro de un Label que está dentro de un contenedor que tiene un Scrollbar. Este es un texto muy largo que se va a mostrar dentro de un Label que está dentro de un contenedor que tiene un Scrollbar. Este es un texto muy largo que se va a mostrar dentro de un Label que está dentro de un contenedor que tiene un Scrollbar. Este es un texto muy largo que se va a mostrar dentro de un Label que está dentro de un contenedor que tiene un Scrollbar. Este es un texto muy largo que se va a mostrar dentro de un Label que está dentro de un contenedor que tiene un Scrollbar. Este es un texto muy largo que se va a mostrar dentro de un Label que está dentro de un contenedor que tiene un Scrollbar. Este es un texto muy largo que se va a mostrar dentro de un Label que está dentro de un contenedor que tiene un Scrollbar. Este es un texto muy largo que se va a mostrar dentro de un Label que está dentro de un contenedor que tiene un Scrollbar. Este es un texto muy largo que se va a mostrar dentro de un Label que está dentro de un contenedor que tiene un Scrollbar."
label = tk.Label(canvas, text=label_text, wraplength=200)
label.pack()

# Configurar el canvas para que contenga el Label
canvas.create_window((0, 0), window=label, anchor="nw")

# Mostrar la ventana principal
root.mainloop()





