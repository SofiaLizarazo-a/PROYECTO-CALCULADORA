import tkinter as tk
from tkinter import colorchooser
import math

# ---------------- VENTANA ----------------
ventana = tk.Tk()
ventana.title("Calculadora Ingeniería Pro")
ventana.geometry("380x780")
ventana.configure(bg="#ffffff")
ventana.resizable(False, False)

# ---------------- VARIABLES ----------------
decimales = 2
botones_lista = []

# ---------------- FUNCIONES DE COLOR ----------------

def hex_a_rgb(hex_color):
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_a_hex(rgb):
    return "#%02x%02x%02x" % rgb

def aclarar_color(hex_color, factor=0.3):
    r, g, b = hex_a_rgb(hex_color)
    r = int(r + (255 - r) * factor)
    g = int(g + (255 - g) * factor)
    b = int(b + (255 - b) * factor)
    return rgb_a_hex((r, g, b))

def color_texto_automatico(hex_color):
    r, g, b = hex_a_rgb(hex_color)
    brillo = (r * 0.299 + g * 0.587 + b * 0.114)
    return "white" if brillo < 128 else "black"

# ---------------- RF06: Logaritmo base arbitraria ----------------

def log_base(base, x):
    if x <= 0:
        raise ValueError("Logaritmo indefinido: argumento debe ser positivo")
    if base <= 0 or base == 1:
        raise ValueError("Logaritmo indefinido: base inválida")
    return math.log(x) / math.log(base)

# ---------------- RF07: Raíz enésima ----------------

def raiz_n(n, x):
    if n == 0:
        raise ValueError("Raíz indefinida: índice no puede ser cero")
    if x < 0:
        if int(n) == n and int(n) % 2 == 1:
            return -((-x) ** (1 / n))
        else:
            raise ValueError("Raíz indefinida: índice par de número negativo")
    return x ** (1 / n)

# ---------------- FUNCIONES CALCULADORA ----------------

def agregar(valor):
    entrada.insert(tk.END, valor)

def limpiar():
    entrada.delete(0, tk.END)

def borrar():
    texto = entrada.get()
    if texto:
        entrada.delete(len(texto) - 1, tk.END)

def parentesis_auto():
    texto = entrada.get()
    if texto.count("(") > texto.count(")"):
        entrada.insert(tk.END, ")")
    else:
        entrada.insert(tk.END, "(")

def calcular():
    global decimales
    try:
        decimales = int(selector_decimales.get())
        expresion = entrada.get()

        expresion = expresion.replace("×", "*")
        expresion = expresion.replace("÷", "/")
        expresion = expresion.replace("^", "**")

        expresion = expresion.replace("logB(", "log_base(")
        expresion = expresion.replace("log(", "math.log10(")
        expresion = expresion.replace("ln(", "math.log(")

        expresion = expresion.replace("raizN(", "raiz_n(")
        expresion = expresion.replace("raiz(", "math.sqrt(")

        resultado = eval(expresion, {"__builtins__": {}}, {
            "math": math,
            "log_base": log_base,
            "raiz_n": raiz_n,
        })

        if isinstance(resultado, float):
            resultado = round(resultado, decimales)

        entrada.delete(0, tk.END)
        entrada.insert(0, str(resultado))

    except ValueError as ve:
        entrada.delete(0, tk.END)
        entrada.insert(0, f"ERROR: {ve}")

    except ZeroDivisionError:
        entrada.delete(0, tk.END)
        entrada.insert(0, "ERROR: División por cero")

    except Exception:
        entrada.delete(0, tk.END)
        entrada.insert(0, "Error")

# ---------------- NUEVO: TECLADO ----------------

def manejar_teclado(event):
    tecla = event.keysym
    char = event.char

    if char in "0123456789.+-*/()%,":
        agregar(char)

    elif tecla == "Return":
        calcular()

    elif tecla == "BackSpace":
        borrar()

    elif tecla == "Escape":
        limpiar()

    elif char == "^":
        agregar("^")

# ---------------- CAMBIAR TEMA ----------------

def cambiar_tema():
    color = colorchooser.askcolor(title="Elegir color")[1]
    if not color:
        return

    ventana.configure(bg=color)
    frame_botones.configure(bg=color)
    frame_decimales.configure(bg=color)

    color_botones = aclarar_color(color, 0.35)
    texto_color = color_texto_automatico(color)

    for b in botones_lista:
        b.configure(bg=color_botones, fg=texto_color, activebackground=color_botones)

    label_decimales.configure(bg=color, fg=texto_color)
    btn_color.configure(bg=color, fg=texto_color)
    selector_decimales.configure(bg=color_botones, fg=texto_color)

# ---------------- PANTALLA ----------------

marco_externo = tk.Frame(ventana, bg="#cfcfcf", bd=3, relief="ridge")
marco_externo.pack(pady=15, padx=20, fill="x")

marco_interno = tk.Frame(marco_externo, bg="#f5f5f5", bd=2, relief="sunken")
marco_interno.pack(fill="both")

entrada = tk.Entry(
    marco_interno,
    font=("Consolas", 22, "bold"),
    bg="white",
    fg="black",
    bd=0,
    justify="right",
    insertbackground="black"
)
entrada.pack(fill="x", ipady=10)

# ---------------- AYUDA ----------------

ayuda = tk.Label(
    ventana,
    text="logB(base,x) | raizN(n,x) | log(x) | ln(x) | raiz(x)",
    font=("Consolas", 8),
    bg="#ffffff",
    fg="#888888"
)
ayuda.pack()

# ---------------- BOTÓN COLOR ----------------

btn_color = tk.Button(
    ventana,
    text="🖌",
    command=cambiar_tema,
    font=("Arial", 16, "bold"),
    bg="#ffffff",
    fg="black",
    bd=0,
    cursor="hand2"
)
btn_color.pack(pady=4)

# ---------------- BOTONES ----------------

frame_botones = tk.Frame(ventana, bg="#ffffff")
frame_botones.pack(pady=8)

botones_extra = ["logB(", "raizN(", "raiz(", ","]

for i, texto in enumerate(botones_extra):
    boton = tk.Button(frame_botones, text=texto, width=7, height=2,
                      font=("Arial", 11, "bold"), command=lambda t=texto: agregar(t))
    boton.grid(row=0, column=i, padx=6, pady=4)
    botones_lista.append(boton)

botones = [
    "%","(","C","⌫",
    "log(","ln(","^","÷",
    "7","8","9","×",
    "4","5","6","-",
    "1","2","3","+",
    "0",".",")","="
]

fila = 1
columna = 0

for texto in botones:
    if texto == "=":
        cmd = calcular
    elif texto == "C":
        cmd = limpiar
    elif texto == "⌫":
        cmd = borrar
    elif texto == "(":
        cmd = parentesis_auto
    else:
        cmd = lambda t=texto: agregar(t)

    boton = tk.Button(frame_botones, text=texto, width=7, height=3,
                      font=("Arial", 12, "bold"), command=cmd)
    boton.grid(row=fila, column=columna, padx=6, pady=6)
    botones_lista.append(boton)

    columna += 1
    if columna > 3:
        columna = 0
        fila += 1

# ---------------- DECIMALES ----------------

frame_decimales = tk.Frame(ventana, bg="#ffffff")
frame_decimales.pack(pady=8)

label_decimales = tk.Label(frame_decimales, text="Decimales:", font=("Arial", 13, "bold"))
label_decimales.pack(side="left", padx=5)

selector_decimales = tk.Spinbox(frame_decimales, from_=0, to=10, width=4, font=("Arial", 13))
selector_decimales.pack(side="left")
selector_decimales.delete(0, "end")
selector_decimales.insert(0, "2")

# ---------------- ACTIVAR TECLADO ----------------
ventana.bind("<Key>", manejar_teclado)

# ---------------- RUN ----------------
ventana.mainloop()