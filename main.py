import pygame
import sys
import motor_mapa #Clase que contiene el mapa base, osea el completo
import Agente_Base

#Esta flag se cambia a True cuando se inicia la partida y se coloree el mapa
partida_iniciada = False

pygame.init()
tamaño_celda = 13
filas, columnas = 50, 50 
ancho, alto = columnas * tamaño_celda, filas * tamaño_celda
pantalla = pygame.display.set_mode((ancho, alto))
pygame.display.set_caption("Proyecto Sistemas Inteligentes - Fase 1")
reloj = pygame.time.Clock()

#COLORES RGB
COLOR_NIEBLA = (20, 20, 40)   # azul muy oscuro (casi negro)
COLOR_SUELO = (220, 220, 220) # Blanco casi puro
COLOR_MURO = (50, 50, 50)     # Gris oscuro
negro = (0, 0, 0)
blanco = (255, 255, 255)
gris = (100, 100, 100)
verde = (0, 255, 0)
azul = (0, 0, 255)

# Dibujar mundo 
def dibujar_mundo(mapa_matriz, entidades):
    # 1. Dibujar todo el mapa
    for f in range(filas):
        for c in range(columnas):
            rect = (c * tamaño_celda, f * tamaño_celda, tamaño_celda, tamaño_celda)
            valor = mapa_matriz[f][c]

            # Dibujar el mapa en base a los numeros
            if valor == -1:
                color = COLOR_NIEBLA
            elif valor == 0:
                color = COLOR_SUELO
            elif valor == 1:
                color = COLOR_MURO
            else:
                color = negro # Por si hay un bug o algo ps aqui se pinta de negro

            pygame.draw.rect(pantalla, color, rect)
            pygame.draw.rect(pantalla, (30,30,30), rect, 1) # Borde para ver la rejilla

            # Dibujar recursos
            if valor == 2:
                pygame.draw.circle(pantalla, verde, (c * tamaño_celda + 7, f * tamaño_celda + 7), 4)

    # 2. Dibujar agentes
    for ent in entidades:
        y, x = ent['pos']
        color = azul if ent['tipo'] == 'jugador' else (255, 0, 0)
        pygame.draw.circle(pantalla, color, (x * tamaño_celda + 7, y * tamaño_celda + 7), 4)


##Las posiciones de origen serviran para que puedan regresar al tomar una de las reliquias
origen_J = [1,1] ##[y, x]
origen_A1 = [1,28]
origen_A2 = [48,1]
origen_A3 = [48,48]

##Posiciones de jugador, 3 agentes y 2 reliquias Iniciales     
arr_posiciones = [
    {'pos': [1, 1], 'tipo': 'jugador'},
    {'pos': [1, 48], 'tipo': 'agente_1'}, 
    {'pos': [48, 1], 'tipo': 'agente_2'},
    {'pos': [48, 48], 'tipo': 'agente_3'}
]

#Inicializar mis clases
a1 = Agente_Base.Agente_1(arr_posiciones[1]['pos'])
a2 = Agente_Base.Agente_2(arr_posiciones[2]['pos'])
a3 = Agente_Base.Agente_3(arr_posiciones[3]['pos'])

while True:
    #Seleccionar vista de J o A, todavia no lo puse jaja pero abajo pongo con que perspectiva se ve


    # --- PARTE A: Eventos (Cerrar ventana, teclas) ---
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # --- PARTE B: Logica de Agentes ---
    #Inicializar mapa de los agentes
    if partida_iniciada == False:
        a1.iniciar_mapa()
        a2.iniciar_mapa()
        a3.iniciar_mapa()
        partida_iniciada = True

    a1.ver_mapa(arr_posiciones)
    a2.ver_mapa(arr_posiciones)
    a3.ver_mapa(arr_posiciones)

    # --- PARTE C: Dibujar, aqui se puede cambiar la perspectiva cambiando de a1 a a2 y a3 Prof xd---
    pantalla.fill(negro)
    dibujar_mundo(a1.mapa_memoria, arr_posiciones)
    #mapa completo
    #dibujar_mundo(motor_mapa.Mapa.mapaI, arr_posiciones)
    pygame.display.flip()

    # --- PARTE D: Decision de agentes ---
    a1.decision_agente(arr_posiciones)
    a2.decision_agente(arr_posiciones)
    a3.decision_agente(arr_posiciones)

    reloj.tick(5)