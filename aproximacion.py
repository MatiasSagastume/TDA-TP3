import pulp


def aproximacion_pl(maestros, k):
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
    for suma in sumatoria:
        problema += maximo >= suma
    problema += maximo
    problema.solve()
    for maestro in maestros:
        for g in grupos:
            if pulp.value(y[(g, maestro)]) > 0:
                res[g].add(maestro)
    return res


maestros = [("Hasook", 120),
            ("Hama", 445),
            ("Senna", 546),
            ("Hama I", 222),
            ("Wei", 551),
            ("Wei I", 330)]

print(aproximacion_pl(maestros, 4))
