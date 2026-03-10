import random
import motor_mapa
import aStar_Algoritmo

filas = len(motor_mapa.Mapa.mapaI[1])
columnas = len(motor_mapa.Mapa.mapaI[0])

class Agente_Base:
    def __init__(self, origen, tipo_agente):
        self.origen = list(origen)
        self.tipo = tipo_agente 
        self.filas = filas
        self.columnas = columnas
        self.mapa_memoria = [] 
        self.cargando_gemas = False  #Se vuelve true cuando en decision esta en una gema
        self.aStar_ruta = []

    def iniciar_mapa(self):
        for f in range(self.filas):
            nueva_fila = []
            for col in range(self.columnas):
                nueva_fila.append(-1)
            self.mapa_memoria.append(nueva_fila)

    def obtener_mi_posicion(self, posiciones):
        for entidad in posiciones:
            if entidad['tipo'] == self.tipo:
                return entidad
        return None

    def ver_mapa(self, posiciones):
        mi_entidad = self.obtener_mi_posicion(posiciones)
        y, x = mi_entidad['pos']
        
        self.mapa_memoria[y][x] = 4
        
        # Bucle para explorar el 3x3 sin salirnos del mapa tremenda logica
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                ny = y + dy
                nx = x + dx
                # Validar que no estemos fuera del mapa
                if 0 <= ny < self.filas and 0 <= nx < self.columnas:
                    self.mapa_memoria[ny][nx] = motor_mapa.Mapa.mapaI[ny][nx]

    def decision_agente(self, posiciones):
        mi_entidad = self.obtener_mi_posicion(posiciones)
        y, x = mi_entidad['pos']
        
        arreglo_posibilidades = []
        arreglo_preferente = []
        arreglo_gema = []
        
        #Direcciones en cruz para no ponerlas manual como lo habia hecho
        direcciones = [
            (-1, 0), (1, 0), (0, -1), (0, 1),
            (-1, -1), (-1, 1), (1, -1), (1, 1)]

        #Toma de decisiones en base a posiciones donde puede moverse
        for dy, dx in direcciones:
            ny = y + dy
            nx = x + dx
            
            if 0 <= ny < 50 and 0 <= nx < 50:
                #Si encuentra la gema guardar la posiscion y después guardarlo como eleccion pref
                if self.mapa_memoria[ny][nx] == 2:
                    arreglo_gema.append([ny, nx])

                    #Lo siguiente refiere a ver si no se desborda 
                    ny_frente = y + (2 * dy)
                    nx_frente = x + (2 * dx)
                    
                    if 0 <= ny_frente < 50 and 0 <= nx_frente < 50:
                        if self.mapa_memoria[ny_frente][nx_frente] == -1:
                            arreglo_preferente.append([ny, nx])

                #Si es un espacio disponible
                elif self.mapa_memoria[ny][nx] == 0:
                    arreglo_posibilidades.append([ny, nx])
                    
                    ny_frente = y + (2 * dy)
                    nx_frente = x + (2 * dx)
                    
                    if 0 <= ny_frente < 50 and 0 <= nx_frente < 50:
                        if self.mapa_memoria[ny_frente][nx_frente] == -1:
                            arreglo_preferente.append([ny, nx])

        # ---  REGLAS PARA LA TOMA DE DECISIONES ---
        # --> Regla para seguir la ruta de vuelta al origen con Gema caso especial POR ENCIMA DE OTRAS RUTAS#
        if self.cargando_gemas == True:
            mi_entidad['pos'] = list(self.aStar_ruta[0])
            self.aStar_ruta.pop(0) # Eliminar a donde nos movimos
            if len(self.aStar_ruta) == 0:
                self.cargando_gemas = False
            return # INDISPENSABLE este return, sino sigue y sobreescribe

        #Preferir que se mueva a la gema y calcular AStar
        if len(arreglo_gema) > 0:
            mi_entidad['pos'] = arreglo_gema[0]
            y,x = arreglo_gema[0]
            motor_mapa.Mapa.mapaI[y][x] = 0
            self.cargando_gemas = True #Estado de cargar para evaluar el AStar
            self.aStar_ruta = aStar_Algoritmo.algoritmo_a_estrella(self.mapa_memoria,arreglo_gema[0],self.origen)
            arreglo_gema.pop(0) # Vaciarlo
            self.aStar_ruta.pop(0) # Porque es la pos donde esta parado
         
        elif len(arreglo_preferente) > 0:
            mi_entidad['pos'] = random.choice(arreglo_preferente)
        elif len(arreglo_posibilidades) > 0:
            mi_entidad['pos'] = random.choice(arreglo_posibilidades)
        else:
            print(f"{self.tipo} está atrapado!")
    


# --- MIS CLASES HIJAS xd ---
class Agente_1(Agente_Base):
    def __init__(self, origen):
        super().__init__(origen, 'agente_1')
class Agente_2(Agente_Base):
    def __init__(self, origen):
        super().__init__(origen, 'agente_2')
class Agente_3(Agente_Base):
    def __init__(self, origen):
        super().__init__(origen, 'agente_3')