from ply import yacc

tokens = (
    'VARIABLE','ENTERO','FLOAT',
    'SUMA','RESTA','MULTIPLICACION','DIVISION','IGUAL',
    'LPARENTESIS','RPARENTESIS','LCORCHETE', 'RCORCHETE'
    )#Estos son los nombres los tokens 

# Tokens se le asigna la simbologia 

t_SUMA           = r'\+'
t_RESTA          = r'-'
t_MULTIPLICACION = r'\*'
t_DIVISION       = r'/'
t_IGUAL          = r'='
t_LPARENTESIS    = r'\('
t_RPARENTESIS    = r'\)'
t_LCORCHETE      = r'\['
t_RCORCHETE      = r'\]'
t_VARIABLE       = r'[a-zA-Z_][a-zA-Z0-9_]*'

#Definimos 
def t_FLOAT(t):
    r'(\d*\.\d+)|(\d+\.\d*)'  #[0-9].[0-9]
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


#Se definen en los tokens
# Ignored characters si no hay
t_ignore = " \t"
#ejemplificamos Anysin
def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
def t_error(t):
    print("Caracter no Valido '%s'" % t.value[0])
    t.lexer.skip(1)
    
# Build the lexer, este es el que le da forma
import ply.lex as lex
lexer = lex.lex()

# Parsing rules---an
#Estos son los que realizan las operaciones
precedence = (
    ('left','SUMA','RESTA'),
    ('left','MULTIPLICACION','DIVISION'),
    ('right','URESTA'),
    )

# dictionary of names--designar v
variable = { }
#se le asigna el valor a variable 
def p_statement_assign(t):
    'statement : VARIABLE IGUAL expression'
    variable[t[1]] = t[3]
#Funcion para las expresiones regulares 
def p_statement_expr(t):
    'statement : expression'
    print(t[1])

#ARBOL DE OPERACIONES BASICAS, por importancia 
def p_expression_binop(t):
    '''expression : expression SUMA expression
                  | expression RESTA expression
                  | expression MULTIPLICACION expression
                  | expression DIVISION expression'''
    if t[2] == '+'  : t[0] = t[1] + t[3]
    elif t[2] == '-': t[0] = t[1] - t[3]
    elif t[2] == '*': t[0] = t[1] * t[3]
    elif t[2] == '/': t[0] = t[1] / t[3]

#Resta para los numeros negativos
def p_expression_uresta(t):
    'expression : RESTA expression %prec URESTA'
    t[0] = -t[2]

#ARBOL DE EXPRESIONES EN PARENTESIS
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

#se vuelve operador, parse realiza las operaciones
parser = yacc.yacc()

#abrimos el archivo 
f = open("texto.txt", "r")

while True:
    linea = f.readline()
    
    if  linea != "":
        print("EXPRESION: " + linea)
        print("TOKENS:")
        analizador = lex.lex ( )
        analizador.input (linea)
        while True :
            tok  =  analizador.token ()
            if not tok  : break
            print ( tok)
            
        
        try:
             s = linea  # Use raw_input on Python 2
        except EOFError:
             break
        print("\n")
        print("RESULTADO:")
        parser.parse(s)

        print("\n")

    if not linea:
        break



f.close()