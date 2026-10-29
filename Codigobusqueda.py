import math
import tkinter as tk
from tkinter import ttk, messagebox

# 1. MATRIZ DE DISTANCIAS (GRAFO DE 28 NODOS)
NUM_NODOS = 28
INF = float('inf')

distancias_raw = [
    [0],
    [908, 0],
    [117, 515, 0],
    [687, 448, 886, 0],
    [1651, 970, 1373, 922, 0],
    [117, 791, 999, 804, 1540, 0],
    [1882, 1013, 117, 1404, 1191, 1765, 0],
    [1310, 441, 844, 832, 529, 1193, 662, 0],
    [889, 246, 684, 202, 720, 840, 1202, 630, 0],
    [760, 181, 559, 479, 997, 643, 1194, 622, 277, 0],
    [2348, 1707, 1811, 1619, 697, 2237, 694, 1223, 1417, 1694, 0],
    [782, 127, 541, 426, 943, 665, 1140, 568, 223, 54, 1640, 0],
    [697, 546, 984, 98, 952, 814, 1502, 930, 300, 577, 1649, 523, 0],
    [1370, 928, 317, 1319, 1463, 1253, 1154, 934, 1117, 774, 1848, 756, 1417, 0],
    [1431, 750, 1153, 702, 220, 1320, 971, 309, 500, 777, 917, 723, 732, 1250, 0],
    [395, 513, 721, 744, 1262, 278, 1407, 915, 542, 365, 1959, 387, 842, 975, 1042, 0],
    [697, 316, 739, 504, 1022, 580, 1329, 757, 302, 180, 1719, 202, 602, 954, 802, 302, 0],
    [1328, 600, 291, 991, 1148, 1211, 826, 606, 789, 729, 1520, 711, 1089, 328, 928, 933, 913, 0],
    [490, 540, 626, 817, 1335, 373, 1553, 981, 615, 392, 2032, 414, 915, 890, 1115, 95, 397, 960, 0],
    [481, 636, 813, 867, 1385, 364, 1610, 1038, 665, 480, 2082, 510, 965, 1077, 1165, 123, 425, 1056, 187, 0],
    [1244, 511, 300, 902, 1046, 1127, 737, 517, 700, 664, 1431, 646, 1000, 417, 826, 849, 844, 89, 895, 972, 0],
    [810, 171, 344, 542, 1029, 693, 1072, 500, 340, 215, 1766, 197, 640, 559, 809, 416, 395, 514, 446, 538, 449, 0],
    [881, 572, 235, 943, 1430, 764, 1352, 901, 741, 616, 2046, 598, 1041, 499, 1210, 486, 796, 526, 391, 578, 615, 401, 0],
    [1145, 460, 898, 416, 506, 1034, 1257, 595, 214, 491, 1203, 437, 446, 1331, 286, 756, 516, 1003, 829, 879, 914, 554, 955, 0],
    [513, 631, 780, 862, 1380, 396, 1605, 1033, 660, 483, 2077, 505, 960, 1044, 1160, 118, 420, 1051, 154, 33, 967, 533, 545, 874, 0],
    [461, 497, 704, 678, 1195, 344, 1432, 938, 476, 349, 1893, 371, 776, 1041, 976, 66, 236, 898, 161, 189, 852, 360, 552, 690, 184, 0],
    [1407, 538, 642, 929, 784, 1290, 475, 255, 727, 719, 1169, 665, 1027, 679, 564, 1012, 854, 351, 1043, 1135, 262, 597, 877, 850, 1130, 957, 0],
    [1000, 131, 534, 522, 839, 883, 882, 310, 320, 312, 1576, 258, 620, 797, 619, 605, 447, 469, 636, 728, 380, 190, 591, 534, 723, 550, 407, 0]
]

grafo = [[0 for _ in range(NUM_NODOS)] for _ in range(NUM_NODOS)]
for i in range(NUM_NODOS):
    for j in range(i + 1):
        costo = distancias_raw[i][j]
        grafo[i][j] = costo
        grafo[j][i] = costo


# 2. ORDENAMIENTO DE OPERADOREs
posiciones = {}
radio = 100
centro = (150, 150)
for i in range(NUM_NODOS):
    angulo = (2 * math.pi * i) / NUM_NODOS
    x = centro[0] + radio * math.cos(angulo)
    y = centro[1] - radio * math.sin(angulo)
    posiciones[i] = (x, y)

def obtener_orden_vecinos(nodo_actual, sentido):
    x_c, y_c = posiciones[nodo_actual]
    vecinos_con_angulo = []
    
    for v in range(NUM_NODOS):
        if v != nodo_actual and grafo[nodo_actual][v] > 0:
            x_v, y_v = posiciones[v]
            ang = math.atan2(y_v - y_c, x_v - x_c)
            vecinos_con_angulo.append((v, ang))
            
    reverse_order = True if sentido == "Sentido del Reloj" else False
    vecinos_con_angulo.sort(key=lambda item: item[1], reverse=reverse_order)
    
    return [v for v, _ in vecinos_con_angulo]

# 3. ALGORITMO DE ESCALADA SIMPLE
def escalada_simple(grafo, inicio, objetivo, sentido):
    nodo_actual = inicio - 1
    nodo_meta = objetivo - 1
    
    if nodo_actual == nodo_meta:
        return [inicio], 0, "El nodo de inicio ya es el estado objetivo."

    camino = [inicio]
    costo_total = 0
    visitados = set([nodo_actual])
    
    logs = []
    logs.append(f"Inicio: Nodo {inicio} -> Meta: Nodo {objetivo}")
    logs.append(f"Dirección de exploración: {sentido}\n")

    def h(nodo):
        return grafo[nodo][nodo_meta]

    while True:
        eval_actual = h(nodo_actual)
        logs.append(f"Estado actual: Nodo {nodo_actual + 1} | h(nodo) = {eval_actual}")
        
        vecinos_ordenados = obtener_orden_vecinos(nodo_actual, sentido)
        movimiento_realizado = False

        for vecino in vecinos_ordenados:
            if vecino in visitados:
                continue

            costo_arista = grafo[nodo_actual][vecino]
            eval_nuevo = h(vecino)

            if vecino == nodo_meta:
                camino.append(vecino + 1)
                costo_total += costo_arista
                logs.append(f" -> ¡Objetivo alcanzado! Moviendo a Nodo {vecino + 1}")
                return camino, costo_total, "\n".join(logs)

            if eval_nuevo < eval_actual:
                logs.append(f" -> Operador aceptado: Moviendo a Nodo {vecino + 1} (h = {eval_nuevo} < {eval_actual})")
                nodo_actual = vecino
                visitados.add(nodo_actual)
                camino.append(nodo_actual + 1)
                costo_total += costo_arista
                movimiento_realizado = True
                break
            else:
                logs.append(f" -> Operador descartado: Nodo {vecino + 1} (h = {eval_nuevo} >= {eval_actual})")

        if not movimiento_realizado:
            logs.append(f"\nATASCADO: Sin mejoras disponibles desde el Nodo {nodo_actual + 1}.")
            return camino, costo_total, "\n".join(logs)


# 4. INTERFAZ GRÁFICA 
def ejecutar_busqueda():
    try:
        inicio = int(combo_inicio.get())
        fin = int(combo_fin.get())
        sentido = combo_sentido.get()

        camino, costo, registro = escalada_simple(grafo, inicio, fin, sentido)

        txt_resultado.delete(1.0, tk.END)
        txt_resultado.insert(tk.END, "=== REGISTRO DE PASOS ===\n" + registro + "\n\n")
        txt_resultado.insert(tk.END, "=== RESUMEN ===\n")
        txt_resultado.insert(tk.END, f"Ruta trazada: {' -> '.join(map(str, camino))}\n")
        txt_resultado.insert(tk.END, f"Costo Acumulado: {costo}\n")
        
        if camino[-1] == fin:
            lbl_status.config(text="Estado: Búsqueda completada con ÉXITO", fg="green")
        else:
            lbl_status.config(text="Estado: Atascado en máximo local", fg="red")

    except ValueError:
        messagebox.showerror("Error de entrada", "Selecciona opciones válidas para todos los campos.")

root = tk.Tk()
root.title("Escalada Simple - Búsqueda en Grafo")
root.geometry("520x580")
root.resizable(False, False)

frame_control = ttk.LabelFrame(root, text=" Configuración de Búsqueda ")
frame_control.pack(padx=10, pady=10, fill="x")

ttk.Label(frame_control, text="Nodo Origen:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
combo_inicio = ttk.Combobox(frame_control, values=[str(i) for i in range(1, NUM_NODOS + 1)], state="readonly", width=10)
combo_inicio.grid(row=0, column=1, padx=5, pady=5)
combo_inicio.current(0)

ttk.Label(frame_control, text="Nodo Destino:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
combo_fin = ttk.Combobox(frame_control, values=[str(i) for i in range(1, NUM_NODOS + 1)], state="readonly", width=10)
combo_fin.grid(row=1, column=1, padx=5, pady=5)
combo_fin.current(10)

ttk.Label(frame_control, text="Sentido de búsqueda:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
combo_sentido = ttk.Combobox(frame_control, values=["Sentido del Reloj", "Sentido Contrarreloj"], state="readonly", width=18)
combo_sentido.grid(row=2, column=1, padx=5, pady=5)
combo_sentido.current(0)

btn_buscar = ttk.Button(frame_control, text="Ejecutar Búsqueda", command=ejecutar_busqueda)
btn_buscar.grid(row=3, column=0, columnspan=2, pady=10)

lbl_status = tk.Label(root, text="Estado: Esperando ejecución...", font=("Arial", 10, "bold"))
lbl_status.pack(pady=2)

frame_salida = ttk.LabelFrame(root, text=" Resultados ")
frame_salida.pack(padx=10, pady=5, fill="both", expand=True)

txt_resultado = tk.Text(frame_salida, wrap="word", width=60, height=18)
txt_resultado.pack(padx=5, pady=5, fill="both", expand=True)

root.mainloop()