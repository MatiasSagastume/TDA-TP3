import time

import greedy1

SALTO_DE_PAGINA = "\n"
SEPARADOR = ", "
POS_HABILIDAD = 1


def backtracking(archivo):
    k, maestros = leer_archivo(archivo)
    aproximacion = greedy1.greedy1(maestros, k)
    res = [aproximacion, calcular_sumatoria_grupo(aproximacion)]  # Empiezo con una aproximacion
    conjuntos = []
    for i in range(k):
        conjuntos.append(set())
    _backtracking(maestros, conjuntos, 0, res)
    return res[0]


def _backtracking(maestros, conjuntos, actual, resultado_actual):
    if esMayor(conjuntos, resultado_actual[1]) or ya_no_llega(conjuntos, resultado_actual[1], actual, maestros):
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


def copiar_grupos(conjuntos):
    res = []
    for g in conjuntos:
        res.append(g.copy())
    return res


def esMayor(nuevo, actual):
    sumatoria_nuevo = calcular_sumatoria_grupo(nuevo)
    return sumatoria_nuevo >= actual

def ya_no_llega(nuevo, actual, n, maestros):
    sumatoria_nuevo = calcular_sumatoria_grupo(nuevo)
    for i in range(n, len(maestros)):
        sumatoria_nuevo += maestros[i][POS_HABILIDAD] ** 2
    return sumatoria_nuevo >= actual


def sumatoria_desde(n, maestros):
    res = 0



def calcular_sumatoria_grupo(grupo):
    res = 0
    for c in grupo:
        res += sumatoria(c) ** 2
    return res

def sumatoria(conj):
    res = 0
    for elemento in conj:
        res += elemento[POS_HABILIDAD]
    return res


def calcular_coeficiente(grupos):
    res = 0
    for g in grupos:
        res += sumatoria(g) ** 2
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


inicio = time.time()
print(calcular_coeficiente(backtracking("CasosCatedra/20_8.txt")))
fin = time.time()
print(fin - inicio)

