import greedy1
def backtracking(maestros, k):
    res = [greedy1.greedy1(maestros, k)] #Empiezo con una aproximacion
    conjuntos = []
    for i in range(k):
        conjuntos.append(set())
    _backtracking(maestros, conjuntos, 0,  res)
    return res[0]


def _backtracking(maestros, conjuntos, actual, resultado_actual):
    if esMayor(conjuntos, resultado_actual[0]):
        return
    if actual == len(maestros):
        if not esMayor(conjuntos, resultado_actual[0]):
            resultado_actual[0] = conjuntos
        return
    for conj in conjuntos:
        conj.add(maestros[actual])
        _backtracking(maestros, conjuntos, actual + 1, resultado_actual)
        conj.remove(maestros[actual])


def esMayor(nuevo, actual):
    sumatoria_nuevo = 0
    sumatoria_actual = 0
    for conj in nuevo:
        sumatoria_nuevo += sumatoria(conj) ** 2
    for conj in actual:
        sumatoria_actual += sumatoria(conj) ** 2
    return sumatoria_nuevo >= sumatoria_actual

def sumatoria(conj):
    res = 0
    for elemento in conj:
        res += elemento[1]
    return res

