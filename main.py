import backtracking
import sys

UBICACION_RUTA = 1
UBICACION_COMANDO = 2
UBICACION_RUTA_GUARDAR = 3
GUARDAR = "-guardar"
TEXTO_GRUPO = "Grupo"
SEPARADOR_GRUPOS = ", "
SEPARADOR = ":"
SALTO_DE_LINEA = "\n"
TEXTO_COEFICIENTE = "Coeficiente: "
MENSAJE_ERROR_PARAMETROS = "Error: parametros insuficientes"
MENSAJE_ERROR_RUTA = "Error: Ruta Inválida"
RUTA_GENERICA = "resultado.txt"
POS_NOMBRE = 0


def main():
    args = sys.argv
    ruta = args[UBICACION_RUTA]
    if len(args) < 1:
        print(MENSAJE_ERROR_PARAMETROS)
        return
    rutaGuardado = None
    if len(args) > 2:
        if args[UBICACION_COMANDO] == GUARDAR:
            rutaGuardado = args[UBICACION_RUTA_GUARDAR]
    grupos = backtracking.backtracking(ruta)
    if not rutaGuardado:
        rutaGuardado = RUTA_GENERICA
    try:
        with open(rutaGuardado, "w") as archivo:
            i = 1
            for g in grupos:
                archivo.write(f"{TEXTO_GRUPO} {i}{SEPARADOR} {unir_grupo(g)}{SALTO_DE_LINEA}")
            archivo.write(f"{TEXTO_COEFICIENTE} {backtracking.calcular_coeficiente(grupos)}")
    except Exception:
        print(MENSAJE_ERROR_RUTA)


def unir_grupo(grupo):
    res = []
    for elem in grupo:
        res.append(elem[POS_NOMBRE])
    return SEPARADOR_GRUPOS.join(res)
