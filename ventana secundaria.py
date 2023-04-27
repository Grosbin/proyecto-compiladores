import tkinter as tk

def open_second_window():
    second_window = tk.Toplevel()
    second_window.title("Segunda ventana")
    second_window.geometry("200x200")

root = tk.Tk()
button = tk.Button(root, text="Abrir segunda ventana", command=open_second_window)
button.pack()
root.mainloop()
