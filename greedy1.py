def greedy1(maestros, k):
    maestros = sorted(maestros)
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

