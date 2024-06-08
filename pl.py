import pulp


def pl(maestros, k):
    problema = pulp.LpProblem("problema", pulp.LpMinimize)
    grupos = range(k)
    nombres = []
    for elem in maestros:
        nombres.append(elem[0])
    y = pulp.LpVariable.dict("maestros", (nombres, grupos), cat=pulp.LpBinary )
    pass
