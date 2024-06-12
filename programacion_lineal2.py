import pulp
import sys

SALTO_DE_PAGINA = "\n"
SEPARADOR = ", "

def main():
    args = sys.argv
    k, maestros = leer_archivo(args[1])
    if k is None or maestros is None:
        print("Error al leer el archivo.")
        return
    nombres = [nombre for nombre, habilidad in maestros]
    habilidades = [habilidad for nombre, habilidad in maestros]
    grupos, diferencia_minima = pl(habilidades, k)
    if grupos is not None:
        grupos_con_nombres = [[nombres[i] for i in grupo] for grupo in grupos]
        print(f"Grupos: {grupos_con_nombres}")
        print(f"Diferencia mínima: {diferencia_minima}")
    else:
        print("No se encontró una solución óptima.")

def pl(maestros, k):
    
    modelo = pulp.LpProblem("DistribucionMaestrosAgua", pulp.LpMinimize)
    
    y = pulp.LpVariable.dicts("y", ((i, j) for i in range(len(maestros)) for j in range(k)), cat=pulp.LpBinary)
    S = pulp.LpVariable.dicts("S", range(k), lowBound=0, cat=pulp.LpContinuous)
    S_max = pulp.LpVariable("S_max", lowBound=0, cat=pulp.LpContinuous)
    S_min = pulp.LpVariable("S_min", lowBound=0, cat=pulp.LpContinuous)
    
    modelo += S_max - S_min
    
    for i in range(len(maestros)):
        modelo += pulp.lpSum(y[i, j] for j in range(k)) == 1
    
    for j in range(k):
        modelo += S[j] == pulp.lpSum(maestros[i] * y[i, j] for i in range(len(maestros)))
    
    for j in range(k):
        modelo += S_max >= S[j]
        modelo += S_min <= S[j]
    
    modelo.solve()
    
    if modelo.status == pulp.LpStatusOptimal:
        grupos = []
        for j in range(k):
            grupo = [i for i in range(len(maestros)) if pulp.value(y[i, j]) > 0.5]
            grupos.append(grupo)
        diferencia_minima = pulp.value(S_max) - pulp.value(S_min)
        return grupos, diferencia_minima
    else:
        return None, None

def leer_archivo(archivo):
    maestros = []
    try:
        with open(archivo) as arch:
            # Leer y descartar la primera línea de comentario
            primera_linea = arch.readline().strip()
            print(f"Primera línea (comentario): {primera_linea}")
            
            # Leer el número de grupos k
            k = int(arch.readline().strip())
            print(f"Número de grupos: {k}")
            
            # Leer cada línea siguiente que contiene el nombre y la habilidad
            for linea in arch:
                linea = linea.strip()
                if linea:
                    print(f"Leyendo línea: {linea}")
                    nombre, habilidad = linea.split(SEPARADOR)
                    maestros.append((nombre.strip(), int(habilidad.strip())))
        return k, maestros
    except FileNotFoundError:
        print(f"Error: el archivo {archivo} no existe.")
        return None, None
    except ValueError as e:
        print(f"Error: formato incorrecto en el archivo {archivo}. Detalle: {e}")
        return None, None

if __name__ == "__main__":
    main()
