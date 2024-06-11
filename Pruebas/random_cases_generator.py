import random

PRIMER_LINEA = "# #La primera linea indica la cantidad de grupos a formar, las siguientes son de la forma 'nombre maestro, habilidad'"
SALTO_DE_LINEA = "\n"


def random_cases_generator(ruta, k):
    indice = 0
    with open(ruta, "w") as archivo:
        archivo.write(PRIMER_LINEA + SALTO_DE_LINEA)
        archivo.write(f"{k}\n")
        suma_grupo = random.randint(600, 3000)
        for i in range(k):
            actual = suma_grupo
            while actual > 0:
                valor = random.randint(int(suma_grupo / 3), suma_grupo)
                if valor > actual:
                    valor = actual
                actual -= valor
                archivo.write(f"{indice}, {valor}" + SALTO_DE_LINEA)
                indice += 1


indice = 0
for i in range(6, 40):
    for n in range(20):
        random_cases_generator(f"casosInmanejables/caso{indice}.txt", i)
        indice += 1
