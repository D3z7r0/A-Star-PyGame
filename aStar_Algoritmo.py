class Nodo:
    def __init__(self, padre=None, posicion=None):
        self.padre = padre
        self.posicion = posicion # Tupla (y, x)
        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, otro):
        return self.posicion == otro.posicion

def algoritmo_a_estrella(mapa, posI, posF):
    """
    Devuelve una lista de coordenadas (rutas) o None si no hay camino.
    inicio y fin deben ser tuplas (y, x)
    """
    # 1. Crear los nodos, la de inicio sera la pos del agente y la final sera el origen
    #La logica es ir iterando para guardar las posiciones recorridas y despues invertirlo
    nodo_inicio = Nodo(None, posI)
    nodo_fin = Nodo(None, posF)

    # 2. Inicializar las listas open y closed
    open_list = []
    closed_list = []

    # 3. Añadir el nodo inicial a la open list
    open_list.append(nodo_inicio)

    # 4. Loop principal hasta encontrar la meta o agotar opciones
    while len(open_list) > 0:
        # a) Obtener el nodo actual (el de menor coste F)
        nodo_actual = open_list[0]
        indice_actual = 0
        for indice, item in enumerate(open_list):
            if item.f < nodo_actual.f:
                nodo_actual = item
                indice_actual = indice

        # b) Sacar el nodo actual de open y meterlo a closed (¡Ya no lo visitará más!)
        open_list.pop(indice_actual)
        closed_list.append(nodo_actual)

        # c) ¿Encontramos la meta? (Reconstruir la ruta hacia atrás)
        if nodo_actual.posicion == tuple(nodo_fin.posicion):
            ruta = []
            actual = nodo_actual
            while actual is not None:
                ruta.append(actual.posicion)
                actual = actual.padre
            return ruta[::-1] # Invertir la ruta para que vaya de Inicio a Fin

        # d) Generar hijos (Nodos adyacentes)
        hijos = []
        direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1)] # Solo cruz 
        
        for dy, dx in direcciones:
            pos_nodo = (nodo_actual.posicion[0] + dy, nodo_actual.posicion[1] + dx)

            # Validar que esté dentro del mapa
            if pos_nodo[0] < 0 or pos_nodo[0] >= len(mapa) or pos_nodo[1] < 0 or pos_nodo[1] >= len(mapa[0]):
                continue

            # Validar que sea un camino transitable (0). Evita muros (1)
            if mapa[pos_nodo[0]][pos_nodo[1]] == -1 or mapa[pos_nodo[0]][pos_nodo[1]] == 1:
                continue

            # Crear nuevo nodo hijo
            nuevo_nodo = Nodo(nodo_actual, pos_nodo)
            hijos.append(nuevo_nodo)

        # e) Evaluar a los hijos
        for hijo in hijos:
            # Si el hijo ya está en la closed list, lo ignoramos (¡Cero ciclos infinitos!)
            if len([cerrado for cerrado in closed_list if cerrado == hijo]) > 0:
                continue

            # Calcular los valores matemáticos G, H y F
            hijo.g = nodo_actual.g + 1
            # Distancia Manhattan
            hijo.h = abs(hijo.posicion[0] - nodo_fin.posicion[0]) + abs(hijo.posicion[1] - nodo_fin.posicion[1])
            hijo.f = hijo.g + hijo.h

            # Si el hijo ya está en la open list y su coste G actual es peor, ignorarlo
            if len([abierto for abierto in open_list if hijo == abierto and hijo.g > abierto.g]) > 0:
                continue

            # Añadir el hijo a la open list para evaluarlo después
            open_list.append(hijo)
            
    # Si el while termina y no retornó la ruta, significa que el agente está encerrado
    return None