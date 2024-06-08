def verificador(maestros, solucion, k, b):
    if len(solucion) > k:
        return False
    sumatoria = 0
    maestros_cubiertos = set()
    maestros = set(maestros)
    for subconj in solucion:
        for elemento in maestros:
            if elemento not in maestros:
                return False
            if elemento in maestros_cubiertos:
                return False
            maestros_cubiertos.add(elemento)
        sumatoria += sum(subconj) ** 2
    return sumatoria <= b and len(maestros_cubiertos) == len(maestros)

