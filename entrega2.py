from itertools import combinations, permutations, product
from simpleai.search import (CspProblem, MOST_CONSTRAINED_VARIABLE, HIGHEST_DEGREE_VARIABLE,LEAST_CONSTRAINING_VALUE, min_conflicts, backtrack)
from collections import Counter

# Debe haber 4 porciones del mismo color entre todos los frascos
def cantidad_mismo_color(variables, values):
    # Contar las apariciones de cada color en todos los frascos
    counter = Counter(color for contenido in values for color in contenido)

    # Verificar que cada color aparezca exactamente 4 veces
    return all(count == 4 for count in counter.values())

#Ningun color debe arrancar con todas sus porciones al fondo
def todas_porciones_color_al_fondo(variables, values):
    # Contar las apariciones del color en la primera posición de cada frasco
    counter = Counter(values[frasco][0] for frasco in variables)

    # Verificar que ningún color aparezca exactamente 4 veces al inicio
    return all(count < 4 for count in counter.values())

# frascos adyacentes deben compartir al menos un color
def frascos_adyacentes_con_color_compartido(variables, values):
    colores1, colores2 = values
    return any(color in colores1 for color in colores2)

#frascos adyacentes deben tener no mas de 6 colores diferentes
def frascos_adyacentes_con_colores_diferentes(variables, values):
    colores1, colores2 = values
    return len(set(list(colores1)+list(colores2))) <= 6

#dos frascos no pueden ser identicos
def frascos_identicos(variables, values):
    frasco1, frasco2 = values
    return frasco1 != frasco2


def generar_restricciones(FRASCOS):
    restricciones = [
        (FRASCOS, todas_porciones_color_al_fondo),
        (FRASCOS, cantidad_mismo_color)
    ]

    # Agregar restricciones para frascos adyacentes
    restricciones.extend(
        ((FRASCOS[x], FRASCOS[x+1]), frascos_adyacentes_con_color_compartido) for x in range(len(FRASCOS) - 1)
    )
    restricciones.extend(
        ((FRASCOS[x], FRASCOS[x+1]), frascos_adyacentes_con_colores_diferentes) for x in range(len(FRASCOS) - 1)
    )

    # Agregar restricciones para frascos no adyacentes
    restricciones.extend(
        ((frasco1, frasco2), frascos_identicos) for frasco1, frasco2 in combinations(FRASCOS, 2)
    )

    return restricciones

#generar frascos por color
def generar_frascos(colores):
    return list(range(len(colores)))

def generar_dominios(frascos, colores, contenido_parcial):
    # Genera combinaciones de 4 colores sin que todos los colores sean iguales
    posibilidades = [p for p in product(colores, repeat=4) if len(set(p)) != 1]

    # Asigna las combinaciones posibles a cada frasco
    dominios = {frasco: posibilidades for frasco in frascos}

    # Genera combinaciones para el contenido parcial
    for n, contenido in enumerate(contenido_parcial):
        extensiones = product(colores, repeat=4 - len(contenido))
        dominios[n] = [tuple(contenido) + ext for ext in extensiones]

    return dominios


def armar_nivel(colores, contenidos_parciales):
    FRASCOS = tuple(generar_frascos(colores))
    DOMINIOS = generar_dominios(FRASCOS, colores, contenidos_parciales)

    restricciones = generar_restricciones(FRASCOS)

    problem = CspProblem(FRASCOS, DOMINIOS, restricciones)
    solution = tuple(min_conflicts(problem).values())

    return solution