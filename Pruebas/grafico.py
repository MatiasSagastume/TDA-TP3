import time

import matplotlib.pyplot as plt
import pulp

import aproximacion

SALTO_DE_PAGINA = "\n"
POS_MINUTO_0 = 0
MINUTO_INICIAL = 1
MAXIMO_INICIAL = 0

MAX_ENEMIGOS = 5000
MAX_RECARGA = 10

TAMANIO_INICIAL = 1
TAMANIO_FINAL = 10000
TAMANIO_SALTO = 100


SEPARADOR = ", "
POS_HABILIDAD = 1


def greedy1(maestros, k):
    maestros = sorted(maestros, key=lambda x: -x[1])
    conjuntos = []
    for i in range(k):
        conjuntos.append(set())
    for elemento in maestros:
        minimo = encontrar_minimo(conjuntos)
        minimo.add(elemento)
    return conjuntos


def encontrar_minimo(conjuntos):
    minimo = conjuntos[0]
    for conj in conjuntos:
        if sumatoria(conj) < sumatoria(minimo):
            minimo = conj
    return minimo


def sumatoria(conj):
    res = 0
    for elemento in conj:
        res += elemento[1]
    return res


def calcular_coeficiente(grupos):
    res = 0
    for g in grupos:
        res += sumatoria(g) ** 2
    return res


def backtracking(archivo):
    k, maestros = leer_archivo(archivo)
    aproximacion = greedy1(maestros, k)
    res = [aproximacion, calcular_sumatoria_grupo(aproximacion)]  # Empiezo con una aproximacion
    conjuntos = []
    for i in range(k):
        conjuntos.append(set())
    _backtracking(maestros, conjuntos, 0, res)
    return res[0]


def _backtracking(maestros, conjuntos, actual, resultado_actual):
    if es_mayor(conjuntos, resultado_actual[1]) or ya_no_llega(conjuntos, resultado_actual[1], actual, maestros):
        return
    if actual == len(maestros):
        nuevo = copiar_grupos(conjuntos)
        resultado_actual[0] = nuevo
        resultado_actual[1] = calcular_sumatoria_grupo(nuevo)
        return
    for conj in conjuntos:
        conj.add(maestros[actual])
        _backtracking(maestros, conjuntos, actual + 1, resultado_actual)
        conj.remove(maestros[actual])
        if not conj:
            break


def copiar_grupos(conjuntos):
    res = []
    for g in conjuntos:
        res.append(g.copy())
    return res


def es_mayor(nuevo, actual):
    sumatoria_nuevo = calcular_sumatoria_grupo(nuevo)
    return sumatoria_nuevo >= actual


def ya_no_llega(nuevo, actual, n, maestros):
    sumatoria_nuevo = calcular_sumatoria_grupo(nuevo)
    for i in range(n, len(maestros)):
        sumatoria_nuevo += maestros[i][POS_HABILIDAD] ** 2
    return sumatoria_nuevo >= actual


def calcular_sumatoria_grupo(grupo):
    res = 0
    for c in grupo:
        res += sumatoria(c) ** 2
    return res


def leer_archivo(archivo):
    maestros = []
    with open(archivo) as arch:
        arch.readline()
        k = int(arch.readline().rstrip(SALTO_DE_PAGINA))
        for linea in arch:
            nombre, habilidad = linea.rstrip(SALTO_DE_PAGINA).split(SEPARADOR)
            maestros.append((nombre, int(habilidad)))
    return k, maestros


def pl(maestros, k):

    modelo = pulp.LpProblem("DistribucionMaestrosAgua", pulp.LpMinimize)

    y = pulp.LpVariable.dicts("y", ((i, j) for i in range(len(maestros)) for j in range(k)), cat=pulp.LpBinary)
    S = pulp.LpVariable.dicts("S", range(k), lowBound=0, cat=pulp.LpContinuous)
    S_max = pulp.LpVariable("S_max", lowBound=0, cat=pulp.LpContinuous)
    S_min = pulp.LpVariable("S_min", lowBound=0, cat=pulp.LpContinuous)

    modelo += S_max - S_min

    for i in range(len(maestros)):
        modelo += pulp.lpSum(y[i, j] for j in range(k)) == 1

    for j in range(k):
        modelo += S[j] == pulp.lpSum(maestros[i] * y[i, j] for i in range(len(maestros)))

    for j in range(k):
        modelo += S_max >= S[j]
        modelo += S_min <= S[j]

    modelo.solve()

    if modelo.status == pulp.LpStatusOptimal:
        grupos = []
        for j in range(k):
            grupo = [i for i in range(len(maestros)) if pulp.value(y[i, j]) > 0.5]
            grupos.append(grupo)
        diferencia_minima = pulp.value(S_max) - pulp.value(S_min)
        return grupos, diferencia_minima
    else:
        return None, None

def graficar_aproximacion_greedy():
    listaTamanios = []
    listaDuraciones = []
    for i in range(2, 6):
        promedio = 0
        for n in range(4):
            caso = f"casosComparacion/caso{i}_{n}.txt"
            k, maestros = leer_archivo(caso)
            resultado_backtracking = calcular_coeficiente(backtracking(caso))
            resultado_greedy = calcular_coeficiente(greedy1(maestros, k))
            promedio += resultado_greedy / resultado_backtracking
        listaTamanios.append(i)
        listaDuraciones.append(promedio / 4)
    plt.figure(figsize=(10, 6))
    plt.plot(listaTamanios, listaDuraciones, marker='o', linestyle='-')
    plt.title('Gráfico de Backtracking vs Greedy')
    plt.xlabel('Cantidad de grupos')
    plt.ylabel('r(A)')
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def graficar_aproximacion_casos_inmanejables_greedy():
    listaTamanios = []
    listaDuraciones = []
    indice = 0
    for i in range(6, 40):
        promedio = 0
        for n in range(20):
            caso = f"casosInmanejables/caso{indice}.txt"
            k, maestros = leer_archivo(caso)
            resultado = k * ((sumatoria(set(maestros)) / k) ** 2)
            resultado_greedy = calcular_coeficiente(greedy1(maestros, k))
            promedio += resultado_greedy / resultado
            indice += 1
        listaDuraciones.append(promedio / 20)
        listaTamanios.append(i)
    plt.figure(figsize=(10, 6))
    plt.plot(listaTamanios, listaDuraciones, marker='o', linestyle='-')
    plt.title('Gráfico de Aproximación Greedy vs Solución Óptima')
    plt.ylabel('r(A)')
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def graficar_tiempo_aproximacion_pl():
    listaTamanios_bt = []
    listaDuraciones_bt = []
    listaTamanios_pl = []
    listaDuraciones_pl = []
    indice = 0
    for i in range(2, 5):
        for n in range(4):
            caso = f"casosComparacion/caso{i}_{n}.txt"
            k, maestros = leer_archivo(caso)
            inicio = time.time()
            backtracking(caso)
            fin = time.time()
            listaDuraciones_bt.append(fin - inicio)
            listaTamanios_bt.append(indice)
            nombres = [nombre for nombre, habilidad in maestros]
            habilidades = [habilidad for nombre, habilidad in maestros]

            inicio = time.time()
            grupos, diferencia_minima = pl(habilidades, k)
            fin = time.time()
            listaDuraciones_pl.append(fin - inicio)
            listaTamanios_pl.append(indice)
            indice += 1
    plt.figure(figsize=(10, 6))
    plt.plot(listaTamanios_bt, listaDuraciones_bt, marker='o', linestyle='-', color="blue")
    plt.plot(listaTamanios_pl, listaDuraciones_pl, marker='o', linestyle='-', color="red")
    plt.title('Comparación de Tiempo Backtracking vs Programación Lineal')
    plt.ylabel('Tiempo (s)')
    plt.grid(True)
    plt.show()


def crear_diccionario_maestros(maestros):
    dic = {}
    for elem in maestros:
        dic[int(elem[0])] = int(elem[1])
    return dic


def graficar_aproximacion_pl():
    listaTamanios = []
    listaDuraciones = []
    indice = 0
    for i in range(2, 6):
        promedio = 0
        for n in range(4):
            caso = f"casosComparacion/caso{i}_{n}.txt"
            k, maestros = leer_archivo(caso)
            sol_optima = calcular_coeficiente(backtracking(caso))
            habilidades = [habilidad for nombre, habilidad in maestros]

            grupos, diferencia_minima = pl(habilidades, k)
            diccionario = crear_diccionario_maestros(maestros)
            valores = []
            for g in grupos:
                nuevo = set()
                for elem in g:
                    nuevo.add((elem, diccionario[elem]))
                valores.append(nuevo)
            sol_pl = calcular_coeficiente(valores)
            indice += 1
            promedio += sol_pl / sol_optima
        listaTamanios.append(i)
        listaDuraciones.append(promedio / 4)
    plt.figure(figsize=(10, 6))
    plt.plot(listaTamanios, listaDuraciones, marker='o', linestyle='-', color="blue")
    plt.title('Backtracking vs Programación Lineal')
    plt.xlabel('Cantidad de grupos')
    plt.ylabel('r(A)')
    plt.grid(True)
    plt.gcf().axes[0].yaxis.get_major_formatter().set_scientific(False)
    plt.show()

def graficar_aproximaciones_pl():
    listaTamanios_pl1 = []
    listaDuraciones_pl1 = []
    listaTamanios_pl2 = []
    listaDuraciones_pl2 = []
    indice = 0
    for i in range(2, 5):
        for n in range(4):
            caso = f"casosComparacion/caso{i}_{n}.txt"
            k, maestros = leer_archivo(caso)
            habilidades = [habilidad for nombre, habilidad in maestros]

            grupos, diferencia_minima = pl(habilidades, k)
            diccionario = crear_diccionario_maestros(maestros)
            valores = []
            for g in grupos:
                nuevo = set()
                for elem in g:
                    nuevo.add((elem, diccionario[elem]))
                valores.append(nuevo)
            sol_pl1 = calcular_coeficiente(valores)
            sol_pl2 = calcular_coeficiente(aproximacion.aproximacion_pl(maestros, k))
            indice += 1
            listaTamanios_pl1.append(indice)
            listaTamanios_pl2.append(indice)
            listaDuraciones_pl1.append(sol_pl1)
            listaDuraciones_pl2.append(sol_pl2)
    plt.figure(figsize=(10, 6))
    plt.plot(listaTamanios_pl1, listaDuraciones_pl1, marker='o', linestyle='-', color="blue")
    plt.plot(listaTamanios_pl2, listaDuraciones_pl2, marker='o', linestyle='-', color="red")
    plt.title('Comparación resultados algoritmos por programación lineal')
    plt.xlabel('Cantidad de grupos')
    plt.ylabel('Coeficiente')
    plt.grid(True)
    plt.show()


def graficar_tiempo_aproximaciones_pl():
    listaTamanios_pl2 = []
    listaDuraciones_pl2 = []
    listaTamanios_pl1 = []
    listaDuraciones_pl1 = []
    indice = 0
    for i in range(2, 6):
        for n in range(4):
            caso = f"casosComparacion/caso{i}_{n}.txt"
            k, maestros = leer_archivo(caso)
            inicio = time.time()
            aproximacion.aproximacion_pl(maestros, k)
            fin = time.time()
            listaDuraciones_pl2.append(fin - inicio)
            listaTamanios_pl2.append(indice)
            habilidades = [habilidad for nombre, habilidad in maestros]
            inicio = time.time()
            pl(habilidades, k)
            fin = time.time()
            listaDuraciones_pl1.append(fin - inicio)
            listaTamanios_pl1.append(indice)
            indice += 1
    plt.figure(figsize=(10, 6))
    plt.plot(listaTamanios_pl2, listaDuraciones_pl2, marker='o', linestyle='-', color="blue")
    plt.plot(listaTamanios_pl1, listaDuraciones_pl1, marker='o', linestyle='-', color="red")
    plt.title('Comparación de Tiempo Algoritmos por Programación Lineal')
    plt.ylabel('Tiempo (s)')
    plt.grid(True)
    plt.show()


def graficar_aproximaciones_vs_greedy():
    listaTamanios_pl = []
    listaDuraciones_pl = []
    listaTamanios_greedy = []
    listaDuraciones_greedy = []
    indice = 0
    for i in range(2, 5):
        for n in range(4):
            caso = f"casosComparacion/caso{i}_{n}.txt"
            k, maestros = leer_archivo(caso)
            sol_pl = calcular_coeficiente(aproximacion.aproximacion_pl(maestros, k))
            sol_greedy = calcular_coeficiente(greedy1(maestros, k))
            indice += 1
            listaTamanios_pl.append(indice)
            listaTamanios_greedy.append(indice)
            listaDuraciones_pl.append(sol_pl)
            listaDuraciones_greedy.append(sol_greedy)
    plt.figure(figsize=(10, 6))
    plt.plot(listaTamanios_pl, listaDuraciones_pl, marker='o', linestyle='-', color="blue")
    plt.plot(listaTamanios_greedy, listaDuraciones_greedy, marker='o', linestyle='-', color="red")
    plt.title('Comparación resultados programación lineal vs greedy')
    plt.xlabel('Cantidad de grupos')
    plt.ylabel('Coeficiente')
    plt.grid(True)
    plt.show()


def graficar_tiempo_aproximaciones_vs_greedy():
    listaTamanios_pl = []
    listaDuraciones_pl = []
    listaTamanios_greedy = []
    listaDuraciones_greedy = []
    indice = 0
    for i in range(2, 5):
        for n in range(4):
            caso = f"casosComparacion/caso{i}_{n}.txt"
            k, maestros = leer_archivo(caso)
            ini = time.time()
            aproximacion.aproximacion_pl(maestros, k)
            fin = time.time()
            listaDuraciones_pl.append(fin - ini)
            ini = time.time()
            greedy1(maestros, k)
            fin = time.time()
            listaDuraciones_greedy.append(fin - ini)
            indice += 1
            listaTamanios_pl.append(indice)
            listaTamanios_greedy.append(indice)
    plt.figure(figsize=(10, 6))
    plt.plot(listaTamanios_pl, listaDuraciones_pl, marker='o', linestyle='-', color="blue")
    plt.plot(listaTamanios_greedy, listaDuraciones_greedy, marker='o', linestyle='-', color="red")
    plt.title('Comparación Tiempo programación lineal vs greedy')
    plt.ylabel('Tiempo (s)')
    plt.grid(True)
    plt.show()


def graficar_backtracking_tiempo():
    listaTamanios = []
    listaDuraciones = []
    indice = 0
    for i in range(2, 6):
        for n in range(4):
            caso = f"casosComparacion/caso{i}_{n}.txt"
            inicio = time.time()
            resultado_backtracking = calcular_coeficiente(backtracking(caso))
            fin = time.time()
            listaTamanios.append(indice)
            listaDuraciones.append((fin - inicio))
            indice += 1
    plt.figure(figsize=(10, 6))
    plt.plot(listaTamanios, listaDuraciones, marker='o', linestyle='-')
    plt.title('Gráfico de Tamaño vs Tiempo')
    plt.ylabel('Tiempo (s)')
    plt.grid(True)
    plt.show()


graficar_tiempo_aproximaciones_vs_greedy()
