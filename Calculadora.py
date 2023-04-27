import ply.lex as lex
import tkinter as tk

from ply import yacc


# Configurar la ventana

root = tk.Tk()

root.title("Calculadora")

# Obtener las dimensiones de la pantalla

screen_width = root.winfo_screenwidth()

screen_height = root.winfo_screenheight()


# Calcular la posición y tamaño de la ventana para que esté centrada en la pantalla

x = (screen_width // 2) - (400 // 2)  # 400 es el ancho de la ventana

y = (screen_height // 2) - (200 // 2)  # 200 es el alto de la ventana

root.geometry('600x400+{}+{}'.format(x, y))

root.configure(bg="#000")


# Configurar el campo de entrada

input_frame = tk.Frame(root, padx=50, pady=20, bg="#333")

input_frame.pack()


input_text = tk.Entry(input_frame, width=90, bg="#333", fg="white",
                      bd=0, highlightthickness=0, insertbackground="white")

input_text.pack()


# Configurar los botones

button_style = {"background": "#007bff", "foreground": "white", "font": (
    "Helvetica", 14), "border": 0, "padx": 0,  "pady": 10, "width": 50}


# Estos son los nombres los tokens

tokens = (

    'VARIABLE', 'ENTERO', 'FLOAT',

    'SUMA', 'RESTA', 'MULTIPLICACION', 'DIVISION', 'IGUAL',

    'LPARENTESIS', 'RPARENTESIS', 'LCORCHETE', 'RCORCHETE'
)


# Tokens se le asigna la simbologia


t_SUMA = r'\+'

t_RESTA = r'-'

t_MULTIPLICACION = r'\*'

t_DIVISION = r'/'

t_IGUAL = r'='

t_LPARENTESIS = r'\('

t_RPARENTESIS = r'\)'

t_LCORCHETE = r'\['

t_RCORCHETE = r'\]'

t_VARIABLE = r'[a-zA-Z_][a-zA-Z0-9_]*'


# Definimos

def t_FLOAT(t):
    r'(\d*\.\d+)|(\d+\.\d*)'  # [0-9].[0-9]

    t.value = float(t.value)
    return t


def t_ENTERO(t):
    r'\d+'

    try:

        t.value = int(t.value)

    except ValueError:

        print("Integer value too large %d", t.value)

        t.value = 0
    return t


# Se definen en los tokens

# Ignored characters si no hay
t_ignore = " \t"


# ejemplificamos Anysin

def t_newline(t):
    r'\n+'

    t.lexer.lineno += t.value.count("\n")


def t_error(t):

    print("Caracter no Valido '%s'" % t.value[0])

    t.lexer.skip(1)


# Build the lexer, este es el que le da forma


lexer = lex.lex()


# Parsing rules---an

# Estos son los que realizan las operaciones
precedence = (

    ('left', 'SUMA', 'RESTA'),

    ('left', 'MULTIPLICACION', 'DIVISION'),

    ('right', 'URESTA'),
)


# dictionary of names--designar v

variable = {}

# se le asigna el valor a variable


def p_statement_assign(t):
    'statement : VARIABLE IGUAL expression'

    variable[t[1]] = t[3]

# Funcion para las expresiones regulares


def p_statement_expr(t):
    'statement : expression'

    print(t[1])


# ARBOL DE OPERACIONES BASICAS, por importancia

def p_expression_binop(t):
    '''expression : expression SUMA expression

                  | expression RESTA expression

                  | expression MULTIPLICACION expression

                  | expression DIVISION expression'''

    if t[2] == '+':
        t[0] = t[1] + t[3]

    elif t[2] == '-':
        t[0] = t[1] - t[3]

    elif t[2] == '*':
        t[0] = t[1] * t[3]

    elif t[2] == '/':
        t[0] = t[1] / t[3]


# Resta para los numeros negativos

def p_expression_uresta(t):
    'expression : RESTA expression %prec URESTA'

    t[0] = -t[2]


# ARBOL DE EXPRESIONES EN PARENTESIS

def p_expression_group(t):
    '''expression : LPARENTESIS expression RPARENTESIS

                  | LCORCHETE expression RCORCHETE'''

    t[0] = t[2]


def p_expression_entero(t):
    '''

        expression : ENTERO
                   '''

    t[0] = t[1]


def p_expression_float(t):
    'expression : FLOAT'

    t[0] = t[1]


def p_expression_variable(t):
    'expression : VARIABLE'

    try:

        t[0] = variable[t[1]]

    except LookupError:

        print("Undefined name '%s'" % t[1])

        t[0] = 0


def p_error(t):

    print("Error de Sintaxis en: '%s'" % t.value)


# se vuelve operador, parse realiza las operaciones
parser = yacc.yacc()


f = open("texto.txt", "r")


calcular_entrada_btn = tk.Button(
    root, text="Calcular entrada", command=lambda: open_second_window("entrada"), **button_style)

calcular_archivo_btn = tk.Button(
    root, text="Calcular archivo txt", command=lambda: open_second_window("archivo"), **button_style)


calcular_entrada_btn.place(relx=0.5, y=100, anchor="center")

calcular_archivo_btn.place(relx=0.5, y=170, anchor="center")

def open_second_window(entrada_run):
    second_window = tk.Toplevel()
    second_window.title("Segunda ventana")
    # second_window.geometry("500x500")
    second_window.configure(bg="#000")
    second_window.geometry('600x400+{}+{}'.format(x, y))

    def calcular(entrada_run):

        entrada = input_text.get()

        # abrimos el archivo

        f = open("texto.txt", "r")

        # tokens_data = ''
        # resultado = ''
        tok_string = ''

        try:
            if entrada_run == "entrada":
                tok_string += f"\nExpresion: {entrada}\n"
                analizador = lex.lex()
                analizador.input(entrada)
                while True:
                    tok = analizador.token()
                    print(tok)
                    print(f"Entrada: {entrada}, Resultado: {eval(entrada)}")
                    if (tok == None):
                        break

                    tok_string += f"{tok}\n"
                    # else:

                    if not tok:
                        break

                    # tokens_data = tok.__str__() + '\n'
                    # tokens_data = f"{tok_string}"
                tok_string += f"Resultado: {eval(entrada)}\n\n"
                tokens_data_label.config(text=str(tok_string))
                print(tok_string)
                # resultado = calc_file(entrada)
                print(entrada)

            elif entrada_run == "archivo":

                while True:

                    linea = f.readline()

                    if linea != "":
                        tok_string += f"\nExpresion: {linea}\n"
                        analizador = lex.lex()
                        analizador.input(linea)
                        while True:
                            tok = analizador.token()
                            print(tok)
                            if (tok != None):

                                tok_string += f"{tok}\n"
                            else:
                                tok_string += f"Resultado: {eval(linea)}\n\n"
                            if not tok:
                                break

                            # tokens_data = tok.__str__() + '\n'
                        # tokens_data = f"{tok_string}"
                        tokens_data_label.config(text=str(tok_string))
                        print(tok_string)

                    if not linea:
                        break

            input_text.delete(0, tk.END)

        except:
            tokens_data_label.config(text="Error en el cálculo")

        # Función que se encarga de configurar la scrollbar
    def scroll_config(*args):
        canvas.configure(scrollregion=canvas.bbox("all"), width=600, height=tokens_data_label.winfo_height()  if entrada_run == 'entrada' else 400)

    # Crear el contenedor
    container = tk.Frame(second_window)
    container.pack()

        # Crear el objeto Scrollbar y asociarlo con el contenedor
    scrollbar = tk.Scrollbar(container, troughcolor="gray", bg="gray", activebackground="darkgray")
    scrollbar.pack(side="right", fill="y")

        # Crear el objeto Canvas para contener el Label y asociarlo con el contenedor y la scrollbar
    canvas = tk.Canvas(container, yscrollcommand=scrollbar.set)
    canvas.pack(side="left", fill="both", expand=True)

        # Configurar la scrollbar para que funcione correctamente
    scrollbar.config(command=canvas.yview)
    canvas.bind("<Configure>", scroll_config)

    tokens_data_label = tk.Label(
        canvas, text="", fg="white", bg="#000", font=("Helvetica", 18), width=45)
    tokens_data_label.pack(side="bottom", pady=20)

    # Configurar el canvas para que contenga el Label
    canvas.create_window((0, 0), window=tokens_data_label, anchor="nw")

    calcular(entrada_run)

# Ejecutar la ventana

root.mainloop()