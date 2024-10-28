import tkinter as tk
from tkinter import messagebox, simpledialog
import random
import networkx as nx
import matplotlib.pyplot as plt


def matrizTam():
    return random.randint(8, 16) 


def matrizAleatoria():
    tam = matrizTam()
    matriz = [[0 for _ in range(tam)] for _ in range(tam)]
    
    for i in range(tam):
        for j in range(i, tam):
            valor = random.randint(0, 1)
            matriz[i][j] = valor
            matriz[j][i] = valor

    return matriz


def matrizPersonalizable():
    tam = matrizTam()
    matriz = [[0 for _ in range(tam)] for _ in range(tam)]
    
    for i in range(tam):
        for j in range(tam):
            while True:
                valor = simpledialog.askstring("Input", f"Fila {i+1}, Columna {j+1} (0 o 1):")
                if valor in ['0', '1']:
                    matriz[i][j] = int(valor)
                    break
                else:
                    messagebox.showerror("Entrada inválida", "Por favor ingrese 0 o 1 únicamente.")
    
    return matriz


def mostrarGrafo():
    global current_matriz, graph_layout
    if not current_matriz:
        messagebox.showerror("Error", "No hay una matriz generada para mostrar.")
        return
    
    G = nx.Graph()
    tam = len(current_matriz)

    for i in range(tam):
        G.add_node(i)

    for i in range(tam):
        for j in range(i, tam):
            if current_matriz[i][j] == 1:
                G.add_edge(i, j)

    if graph_layout is None:
        graph_layout = nx.spring_layout(G)  # Only generate layout once

    nx.draw(G, graph_layout, with_labels=True, node_color='skyblue', edge_color='black', node_size=1000, font_size=15)
    plt.show()


def calcularCaminoMinimo():
    vertice1 = simpledialog.askinteger("Seleccionar vértice", "Ingrese el primer vértice:")
    vertice2 = simpledialog.askinteger("Seleccionar vértice", "Ingrese el segundo vértice:")

    if vertice1 is not None and vertice2 is not None:
        G = nx.Graph()
        tam = len(current_matriz)

        for i in range(tam):
            for j in range(i, tam):
                if current_matriz[i][j] == 1:
                    G.add_edge(i, j)

        if nx.has_path(G, vertice1, vertice2):
            camino_minimo = nx.shortest_path(G, vertice1, vertice2)
            resultado_text.insert(tk.END, f"\nCamino mínimo entre {vertice1} y {vertice2}: {camino_minimo}\n")
        else:
            resultado_text.insert(tk.END, f"\nNo existe un camino entre {vertice1} y {vertice2}\n")
    else:
        resultado_text.insert(tk.END, "\nVértices no válidos. Por favor, intente nuevamente.\n")


def op1():
    global current_matriz, graph_layout
    current_matriz = matrizAleatoria()
    graph_layout = None  # Reset layout for new graph
    resultado_text.delete(1.0, tk.END) 
    resultado_text.insert(tk.END, "Matriz Aleatoria Generada:\n")
    for fila in current_matriz:
        resultado_text.insert(tk.END, f"{fila}\n")
    btn_mostrar_grafo.config(state=tk.NORMAL)


def op2():
    global current_matriz, graph_layout
    current_matriz = matrizPersonalizable()
    graph_layout = None  # Reset layout for new graph
    resultado_text.delete(1.0, tk.END)  
    resultado_text.insert(tk.END, "Matriz Personalizada Generada:\n")
    for fila in current_matriz:
        resultado_text.insert(tk.END, f"{fila}\n")
    btn_mostrar_grafo.config(state=tk.NORMAL)


def op3():
    root.quit()


root = tk.Tk()
root.title("Programa de Matrices")
root.geometry("500x450")

current_matriz = None
graph_layout = None  # Variable to store the graph layout

frame_buttons = tk.Frame(root)
frame_buttons.pack(pady=20)

btn_op1 = tk.Button(frame_buttons, text="Generar Matriz Aleatoria", command=op1, width=25, height=2, bg="lightblue")
btn_op1.grid(row=0, column=0, padx=5, pady=5)

btn_op2 = tk.Button(frame_buttons, text="Generar Matriz Personalizada", command=op2, width=25, height=2, bg="lightgreen")
btn_op2.grid(row=1, column=0, padx=5, pady=5)

btn_mostrar_grafo = tk.Button(frame_buttons, text="Mostrar Grafo", command=mostrarGrafo, width=25, height=2, bg="lightyellow", state=tk.DISABLED)
btn_mostrar_grafo.grid(row=2, column=0, padx=5, pady=5)

btn_camino_minimo = tk.Button(frame_buttons, text="Calcular Camino Mínimo", command=calcularCaminoMinimo, width=25, height=2, bg="lightcoral")
btn_camino_minimo.grid(row=3, column=0, padx=5, pady=5)

btn_op3 = tk.Button(frame_buttons, text="Salir", command=op3, width=25, height=2, bg="salmon")
btn_op3.grid(row=4, column=0, padx=5, pady=5)

resultado_text = tk.Text(root, height=10, width=60, wrap='word')
resultado_text.pack(pady=10)

root.mainloop()
