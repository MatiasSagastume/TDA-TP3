import random

PRIMER_LINEA = "# #La primera linea indica la cantidad de grupos a formar, las siguientes son de la forma 'nombre maestro, habilidad'"
SALTO_DE_LINEA = "\n"


def random_cases_generator(ruta, k):
    indice = 0
    with open(ruta, "w") as archivo:
        archivo.write(PRIMER_LINEA + SALTO_DE_LINEA)
        archivo.write(f"{k}\n")
        for i in range(3 * k):
            valor = random.randint(0, 2000)
            archivo.write(f"{indice}, {valor}" + SALTO_DE_LINEA)
            indice += 1

indice = 0
for i in range(2, 5):
    for n in range(20):
        random_cases_generator(f"casosComparacion/caso{i}_{n}.txt", i)
        indice += 1

