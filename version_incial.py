import pygame
import random
import time
import os

# Inicializar pygame para sonido
pygame.mixer.init()

# Cargar música de fondo y sonido de victoria
pygame.mixer.music.load("Fondo.mp3")  # Música de fondo
sonido_victoria = pygame.mixer.Sound("Victoria.mp3")  # Sonido al ganar

# -------------------- Reglas del juego --------------------

def mostrar_reglas():

    print("\n                                   ⫘⫘⫘⫘⫘⫘ Tres En Raya ⫘⫘⫘⫘⫘")
    print("\n⫘⫘⫘⫘⫘⫘ REGLAS ⫘⫘⫘⫘⫘")
    print("① Dos jugadores se turnan para jugar.")
    print("② El primer jugador elige si quiere usar 'X' o 'O'.")
    print("③ El objetivo es formar una línea recta de 3 marcas (horizontal, vertical o diagonal).")
    print("④ Para jugar, ingresa el número de celda en la que quieres poner tu marca.")
    print("⑤ El ganador será el primero en formar la línea.")
    print("⑥ Si se llenan las casillas sin que nadie forme la línea de 3 marcas, será empate.")
    print("\nↈↈↈↈↈↈↈↈↈↈↈↈↈↈↈↈↈↈↈↈↈↈↈↈↈↈↈ\n")

# -------------------- Tablero --------------------

def mostrar_tablero(tablero):
    print()
    print(f" {tablero[0]} | {tablero[1]} | {tablero[2]} ")
    print("---|---|---")
    print(f" {tablero[3]} | {tablero[4]} | {tablero[5]} ")
    print("---|---|---")
    print(f" {tablero[6]} | {tablero[7]} | {tablero[8]} ")
    print()

# -------------------- Verificar ganador --------------------

def hay_ganador(tablero, simbolo):
    combinaciones = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # filas
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columnas
        [0, 4, 8], [2, 4, 6]              # diagonales
    ]
    for combo in combinaciones:
        if all(tablero[i] == simbolo for i in combo):
            return True
    return False

def tablero_lleno(tablero):
    return all(c in ['X', 'O'] for c in tablero)


# -------------------- Juego principal --------------------

def jugar_tres_en_raya():
    mostrar_reglas()

    puntos = {"Jugador 1": 0, "Jugador 2": 0}
    ranking = {}

    jugador1 = input("∰ Jugador 1, ¿cómo te llamas (no utilices espacios e incluye apellido)? ").upper()
    jugador2 = input("∰ Jugador 2, ¿cómo te llamas (no utilices espacios e incluye apellido)? ").upper()
    os.system('cls')
    ARCHIVO = 'marcador_tres_en_raya.txt'
    if os.path.exists(ARCHIVO):
        with open(ARCHIVO, 'r') as archivo:
            for linea in archivo:
                linea_lista = linea.split()
                ranking[linea_lista[0]] = linea_lista[1]
            for elemento in ranking:
                if (jugador1 == elemento):
                    while True:
                        pregunta = input(f"El nombre {elemento} ya se encuentra registrado con {ranking[elemento]} victoria(s).\n ¿Eres tú? (si/no): ").upper()
                        if (pregunta == "SI"):
                            break
                        elif (pregunta == "NO"):
                            jugador1 = input(f"∰ Jugador 1, selecciona un nombre distinto de '{elemento}' (no utilices espacios): ").upper()
                            break
                        else: 
                            print("Respuesta inválida. Intentelo de nuevo.")
                            continue
                elif (jugador2 == elemento):
                    while True:
                        pregunta = input(f"El nombre {elemento} ya se encuentra registrado con {ranking[elemento]} victoria(s).\n ¿Eres tú? (si/no): ").upper()
                        if (pregunta == "SI"):
                            break
                        elif (pregunta == "NO"):
                            jugador2 = input(f"∰ Jugador 2, selecciona un nombre distinto de '{elemento}' (no utilices espacios): ").upper()
                            break
                        else: 
                            print("Respuesta inválida. Intentelo de nuevo.")
                            continue

    simbolo1 = ""
    while simbolo1 not in ['X', 'O']:
        simbolo1 = input(f"{jugador1}, elige tu símbolo (X o O): ").upper()

    simbolo2 = 'O' if simbolo1 == 'X' else 'X'

    print(f"{jugador1} jugará con '{simbolo1}' y {jugador2} con '{simbolo2}'\n")

    # Iniciar la música de fondo en bucle
    pygame.mixer.music.play(-1)
    os.system('cls')
    while True:
        tablero = [str(i+1) for i in range(9)]
        turno = 0  # 0 para jugador1, 1 para jugador2

        mostrar_tablero(tablero)

        while True:
            jugador = jugador1 if turno == 0 else jugador2
            simbolo = simbolo1 if turno == 0 else simbolo2

            try:
                movimiento = int(input(f"{jugador} ({simbolo}), elige una casilla (1-9): "))
                if movimiento < 1 or movimiento > 9 or tablero[movimiento - 1] in ['X', 'O']:
                    print("Movimiento inválido. Intenta de nuevo.")
                    continue
            except ValueError:
                print("Por favor, ingresa un número válido.")
                continue

            tablero[movimiento - 1] = simbolo
            os.system('cls')
            mostrar_tablero(tablero)

            if hay_ganador(tablero, simbolo):
                sonido_victoria.play()  # Efecto de victoria
                print(f"🎉 ¡{jugador} ha ganado esta ronda!")
                if turno == 0:
                    puntos["Jugador 1"] += 1
                else:
                    puntos["Jugador 2"] += 1
                time.sleep(2)  # Esperar mientras suena la victoria
                break
            elif tablero_lleno(tablero):
                print("🤝 ¡Empate!")
                break
            else:
                turno = 1 - turno  # Cambiar de turno

        # Mostrar marcador
        ARCHIVO = 'marcador_tres_en_raya.txt'
        if not os.path.exists(ARCHIVO):
            libreria = {}
            with open(ARCHIVO, 'w') as archivo:
                archivo.write(
                    f"{jugador1} {puntos['Jugador 1']}\n"
                    f"{jugador2} {puntos['Jugador 2']}\n"
                    )
            with open(ARCHIVO, 'r') as archivo:
                for linea in archivo:
                    linea_lista = linea.split()
                    libreria[linea_lista[0]] = linea_lista[1]
                print("===== MARCADOR =====")
                for nombre in libreria:
                    print(f"{nombre}: {libreria[nombre]} punto(s)")
                print("====================\n")
        else:
            libreria = {}
            with open(ARCHIVO, 'r') as archivo:
            #Extraer elementos del ARCHIVO a la libreria
                for linea in archivo:
                    linea_lista = linea.split()
                    libreria[linea_lista[0]] = int(linea_lista[1])
            #Ingresar personas a la librería.
                if (jugador1 not in libreria):
                    libreria[jugador1]=0
                if (jugador2 not in libreria):
                    libreria[jugador2]=0
            #Actualizar puntos
                if (jugador1 in libreria):
                        libreria[jugador1] += puntos['Jugador 1']
                if(jugador2 in libreria):
                        libreria[jugador2] += puntos['Jugador 2']
            #Escribir librería actualizada en el ARCHIVO.
                with open(ARCHIVO, 'w') as archivo:
                    for element in libreria:
                        archivo.write(f"{element} {libreria[element]}\n")
            #Imprimir marcador
                print("===== MARCADOR =====")
                for clave in libreria:
                    print(f"{clave}: {libreria[clave]} punto(s)")
                print("====================\n")
    #Reiniciar puntaje
        puntos = {"Jugador 1": 0, "Jugador 2": 0}
        # ¿Jugar otra ronda?
        
        while True:
            otra = input("¿Quieres jugar otra ronda? (si/no): ").lower()
            if otra == 'si':
                break
            elif otra == 'no':
                print("Gracias por jugar. ¡Hasta la próxima!")
                print("\n ===== Creadores===== ")
                print("Antonio Barragán")
                print("Ignacio Jaramillo")
                print("Jose Noboa")
                print("Marcelo Damian")
                pygame.mixer.music.stop()
                return
            else:
                print("Por favor, ingresa 'si' o 'no'.")
# -------------------- Ejecutar --------------------

if __name__ == "__main__":
    jugar_tres_en_raya()
