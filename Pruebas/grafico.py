import time

import matplotlib.pyplot as plt
import pulp

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
    problema = pulp.LpProblem("problema", pulp.LpMinimize)
    grupos = range(k)
    res = []
    for g in grupos:
        res.append(set())
    y = pulp.LpVariable.dict("maestros", (grupos, maestros), cat=pulp.LpBinary)
    for maestro in maestros:
        ecuacion = 0
        for g in grupos:
            ecuacion += y[(g,maestro)]
        problema += ecuacion == 1
    sumatoria = []
    for g in grupos:
        sumatoria.append(pulp.lpSum([y[(g, maestro)] * maestro[1] for maestro in maestros]))
    maximo = pulp.LpVariable("GRUPO_MAX", cat=pulp.LpInteger)
    minimo = pulp.LpVariable("GRUPO_MIN", cat=pulp.LpInteger)
    for suma in sumatoria:
        problema += maximo >= suma
        problema += minimo <= suma
    problema += maximo - minimo
    problema.solve()
    for maestro in maestros:
        for g in grupos:
            if pulp.value(y[(g, maestro)]) > 0:
                res[g].add(maestro)
    return res


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


def graficar_aproximacion_pl():
    listaTamanios = []
    listaDuraciones = []
    indice = 0
    for i in range(2, 5):
        for n in range(20):
            caso = f"casosComparacion/caso{i}_{n}.txt"
            k, maestros = leer_archivo(caso)
            resultado_backtracking = calcular_coeficiente(backtracking(caso))
            resultado_pl = calcular_coeficiente(pl(maestros, k))
            listaDuraciones.append(resultado_pl / resultado_backtracking)
            listaTamanios.append(indice)
            indice += 1
    plt.figure(figsize=(10, 6))
    plt.plot(listaTamanios, listaDuraciones, marker='o', linestyle='-')
    plt.title('Gráfico de Backtracking vs Programación Lineal')
    plt.ylabel('r(A)')
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


graficar_aproximacion_casos_inmanejables_greedy()