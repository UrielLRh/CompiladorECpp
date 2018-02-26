# Uriel Avila Vargas
# A00815578
# Tarea 3 - ply

import ply.lex as lex
import ply.yacc as yacc
import sys

# Variable que indica si esta correcta la entrada
bCorrecto = True

# Tokens
tokens = [
    'MAS', 'MENOS', 'MULTI', 'DIV','MENOR', 'MAYOR', 'DIFER', 'IGUAL',
    'DOSPUNTOS','PUNTOYCOMA', 'COMA', 'PAREN_IZQ','PAREN_DER',
    'LLAVE_IZQ', 'LLAVE_DER', 'ID', 'STRING', 'CTE_INT','CTE_FLOAT'
]

palabras_reservadas = {
    'int'   	: 'VAR_INT',
    'float' 	: 'VAR_FLOAT',
    'var' 	: 'VAR',
    'program' 	: 'PROGRAM',
    'print' 	: 'PRINT',
    'if'	: 'IF',
    'else'	: 'ELSE'
}

# Tokens
t_MAS = r'\+'
t_MENOS = r'\-'
t_MULTI = r'\*'
t_DIV = r'\/'
t_MENOR = r'\<'
t_MAYOR = r'\>'
t_DIFER = r'\<\>'
t_IGUAL = r'\='
t_DOSPUNTOS = r'\:'
t_PUNTOYCOMA = r'\;'
t_COMA = r'\,'
t_PAREN_IZQ = r'\('
t_PAREN_DER = r'\)'
t_LLAVE_IZQ = r'\{'
t_LLAVE_DER = r'\}'
t_STRING = r'\"(\\.|[^"])*\"|\"\"'
t_CTE_INT = r'[0-9]+'
t_CTE_FLOAT = r'[0-9]+\.[0-9]+'

# Tokens + palabras reservadas
tokens = tokens + list(palabras_reservadas.values())

# ID's
def t_ID(t):
    r'[a-zA-Z][a-zA-Z0-9]*'
    t.type = palabras_reservadas.get(t.value,'ID')
    return t

# Caracteres que no se toman en cuenta
t_ignore = ' \t\n'

# Caracteres invalidos
def t_error(t):
    global bCorrecto
    bCorrecto = False
    print("Caracter invalido '%s'" % t.value[0])
    t.lexer.skip(1)

# Construcion del lexer
lex.lex()

# Reglas
def p_programa(t):
    'programa : PROGRAM ID PUNTOYCOMA programaAx bloque'
def p_programaAx(t):
    '''programaAx :  vars
                   | empty'''

def p_vars(t):
    'vars : VAR varsP DOSPUNTOS tipo PUNTOYCOMA varsPPP'
def p_varsP(t):
    'varsP : ID varsPP'
def p_varsPP(t):
    '''varsPP : COMA varsP
              | empty'''
def p_varsPPP(t):
    '''varsPPP :  vars
                | empty'''

def p_tipo(t):
    '''tipo :  VAR_INT
             | VAR_FLOAT'''

def p_bloque(t):
    'bloque : LLAVE_IZQ list_estatutos LLAVE_DER'
def p_list_estatutos(t):
    '''list_estatutos :  estatuto list_estatutos
                       | empty'''

def p_estatuto(t):
    '''estatuto : asignacion
                | condicion
                | escritura'''

def p_asignacion(t):
    'asignacion : ID IGUAL expresion PUNTOYCOMA'

def p_escritura(t):
    'escritura : PRINT PAREN_IZQ escrituraP PAREN_DER PUNTOYCOMA'
def p_escrituraP(t):
    '''escrituraP : expresion escrituraPP
                  | STRING escrituraPP'''
def p_escrituraPP(t):
    '''escrituraPP : COMA escrituraP
                   | empty'''

def p_expresion(t):
    'expresion : exp expresionP'
def p_expresionP(t):
    '''expresionP : expresionPP exp
                  | empty'''
def p_expresionPP(t):
    '''expresionPP : MAYOR
                   | MENOR
                   | DIFER'''

def p_exp(t):
    'exp : termino mas_terminos'
def p_mas_terminos(t):
    '''mas_terminos :  op_termino exp
                     | empty'''
def p_op_termino(t):
    '''op_termino :  MAS
                   | MENOS'''

def p_termino(t):
    'termino : factor terminoP'
def p_terminoP(t):
    '''terminoP : terminoPP termino
                | empty'''
def p_terminoPP(t):
   '''terminoPP : MULTI
                | DIV'''

def p_factor(t):
    '''factor : PAREN_IZQ expresion PAREN_DER
              | op_opcional var_constante'''
def p_op_opcional(t):
    '''op_opcional :  MAS
               		| MENOS
               		| empty'''

def p_var_constante(t):
    '''var_constante : ID
               | CTE_INT
               | CTE_FLOAT'''

def p_condicion(t):
    'condicion : IF PAREN_IZQ expresion PAREN_DER bloque condicionP PUNTOYCOMA'
def p_condicionP(t):
    '''condicionP : ELSE bloque
                  | empty'''

# Vacio (epsilon)
def p_empty(t):
    'empty :'

# Error de sintaxis 
def p_error(t):
    global bCorrecto
    bCorrecto = False
    print("Error de sintaxis en '%s'" % t.value)
    sys.exit()

# Creacion del parser
parser = yacc.yacc()

# Lectura de archivo
nombreArchivo = raw_input("Nombre del archivo: ")
archivo = open(nombreArchivo, 'r')
contenidoArch = archivo.read()
parser.parse(contenidoArch)    

# Notificar si el archivo esta correcto o no
if bCorrecto == True:
    print("Archivo correcto")
    raw_input()
    sys.exit()
else: 
    print("Archivo incorrecto")
    raw_input()
    sys.exit()
