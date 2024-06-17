import tkinter as tk

# Emojis para representar al gato y al ratón
EMOJI_GATO = "😺"
EMOJI_RATON = "🐭"

# Función para obtener todos los movimientos posibles
def obtener_todos_los_movimientos_posibles(jugador, posicion, historial):

    # Direcciones de movimiento: arriba, abajo, izquierda, derecha
    direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    movimientos = []  # Lista para almacenar movimientos posibles
    posicion_actual = posicion[jugador]  # Obtener la posición actual del jugador
    
    for direccion in direcciones: #iteramos en direcciones y agregamos las posiciones en direccion como tuplas

        # Calculamos la nueva posición sumando la dirección actual a la posición actual del jugador.
        nueva_posicion = (posicion_actual[0] + direccion[0], posicion_actual[1] + direccion[1])

        # Verificar que la nueva posición esté dentro del tablero. La fila y la columna
        if 0 <= nueva_posicion[0] < 5 and 0 <= nueva_posicion[1] < 5:

            # Comprueba si el jugador ha visitado la nueva_posicion menos de 2 veces.
            if historial[jugador].count(nueva_posicion) < 2:

                # Crear una variable para almacenar la copia de la posicion 
                nueva_posicion_dict = posicion.copy()
                
                # Actualizar la posición del jugador con la nueva posición
                nueva_posicion_dict[jugador] = nueva_posicion

                # Agregar el nuevo movimiento a la lista
                movimientos.append(nueva_posicion_dict)
    
    return movimientos

# Función para verificar si el juego ha terminado
def es_fin_del_juego(posicion):

    return posicion['gato'] == posicion['raton']  # El juego termina si el gato atrapa al ratón

# Función para evaluar la posición
def evaluar(posicion):

    if posicion['gato'] == posicion['raton']:  # Si el gato atrapó al ratón

        return -10  # Puntuación negativa
    
    return 10  # De lo contrario, puntuación positiva


# Algoritmo Minimax con profundidad limitada
def minimax(posicion, profundidad, es_jugador_maximizador, historial, profundidad_maxima=3):

    if es_fin_del_juego(posicion) or profundidad >= profundidad_maxima:

        return evaluar(posicion)  # Evaluar la posición si el juego terminó o se alcanzó la profundidad máxima
    

    # Turno del ratón
    if es_jugador_maximizador:  # Establecemos el valor de este parametro, o sea el argumento

        mejor = -float('inf')  # Iniciar mejor puntuación como menos infinito

        for movimiento in obtener_todos_los_movimientos_posibles('raton', posicion, historial):

            nuevo_historial = {k: v[:] for k, v in historial.items()} 
             # Verificamos el historial con el metodo .items y obtenemos las tuplas la clave y su valor que representan k y v, y las copiamos al nuevo_historial con [:].

            nuevo_historial['raton'].append(movimiento['raton'])  # Agregar nuevo movimiento al historial
            
            #obtenemos el valor de la puntuacion llamando a la funcion minimax, y dandole argumentos para que pueda obtener por ese medio la mejor puntuacion
            valor = minimax(movimiento, profundidad + 1, False, nuevo_historial, profundidad_maxima)  # Llamada recursiva

            mejor = max(mejor, valor)  # Actualizar mejor puntuación. Si valor es mejor que mejor, actualiza la posicion. 

        return mejor
    
    else:  # Turno del gato
        mejor = float('inf')  # Iniciar mejor puntuación como más infinito

        for movimiento in obtener_todos_los_movimientos_posibles('gato', posicion, historial):

            nuevo_historial = {k: v[:] for k, v in historial.items()}  # Copiar el historial

            nuevo_historial['gato'].append(movimiento['gato'])  # Agregar nuevo movimiento al historial

            valor = minimax(movimiento, profundidad + 1, True, nuevo_historial, profundidad_maxima)  # Llamada recursiva

            mejor = min(mejor, valor)  # Actualizar mejor puntuación

        return mejor

# Definimos la posición inicial del gato y el ratón
posicion_inicial = {
    'gato': (0, 0),
    'raton': (4, 4)
}

# Historial de posiciones inicial
historial_inicial = {
    'gato': [(0, 0)],
    'raton': [(4, 4)]
}

# Clase para la interfaz gráfica del juego
class JuegoGatoRaton:

    def __init__(self, root): # llamo al metodo constructor, y defino las instancias del juego
        self.root = root  # Definimos la referencia a la ventana principal(la base del juego). Con el prefijo self

        self.root.title("Juego del Gato y el Ratón")  # Título de la ventana o base
        
        # Crear el tablero como un canvas que mide 500x500 píxeles, y lo asociamos a la ventana principal (root)
        self.tablero = tk.Canvas(root, width=500, height=500)
        self.tablero.pack()  # Empacar y enviar el canvas en la ventana principal con .pack()
        
        self.dibujar_tablero()  # Dibujar el tablero

        # Inicializar posiciones del gato y el ratón
        self.posicion_gato = posicion_inicial['gato'] #las posiciones se guaran en la variable de instancia self.posicion_gato para que luego se pueda modificar

        self.posicion_raton = posicion_inicial['raton']

        self.historial = {k: v[:] for k, v in historial_inicial.items()}  # Copiar el historial inicial
        
        self.actualizar_tablero()  # Actualizar la visualización del tablero
        
        self.turno = 1  # Inicializar el contador de turnos
        
        self.jugar()  # Iniciar el juego

    def dibujar_tablero(self):

        for i in range(5): #definimos el tamaño del tablero. 'i' representa fila
            for j in range(5):  # Iterar sobre los índices de las columnas (de 0 a 4) 'j' representa columnas 
                # Dibujar rectángulos de 100x100 píxeles para cada celda del tablero

                self.tablero.create_rectangle(100*i, 100*j, 100*(i+1), 100*(j+1), outline="black")  #Método de Tkinter para dibujar un rectángulo en el canvas. y le asignamos un color negro al borde
    
    def actualizar_tablero(self):
        
        self.tablero.delete("gato")  # Borrar el gato del tablero

        self.tablero.delete("raton")  # Borrar el ratón del tablero

        # Dibujar el gato en su nueva posición. Multiplicamos por 100 y sumamos 50 para centrar el emoji dentro de la celda. Llamamos a la variable que asignamos, le ponemos una fuente, tamaño y una etiqueta
        self.tablero.create_text(100*self.posicion_gato[1]+50, 100*self.posicion_gato[0]+50, text=EMOJI_GATO, font=("Helvetica", 36), tags="gato")

        # Dibujar el ratón en su nueva posición
        self.tablero.create_text(100*self.posicion_raton[1]+50, 100*self.posicion_raton[0]+50, text=EMOJI_RATON, font=("Helvetica", 36), tags="raton")
    
    def jugar(self): #llamamos a la funcion jugar para que el juego empiece y los turnos de alternen entre jugadores

        if es_fin_del_juego({'gato': self.posicion_gato, 'raton': self.posicion_raton}):  # Verificar si el juego terminó
            self.mostrar_mensaje_final("¡El gato ha atrapado al ratón!")
            # Mostrar mensaje si el gato atrapó al ratón

            return
        
        # Turno del ratón
        mejor_puntuacion = -float('inf')  # Verifica la mejor puntuación como menos infinito, para asegurarnos de que cualquier puntuacion calculada, sea mejor

        mejor_movimiento = None #almacenamos aqui el mejor movimiento encontrado

        for movimiento in obtener_todos_los_movimientos_posibles('raton', {'gato': self.posicion_gato, 'raton': self.posicion_raton}, self.historial): #aca generamos todas las nuevas posiciones para el raton

            nuevo_historial = {k: v[:] for k, v in self.historial.items()}  # Copiar el historial, en una nueva varianle, asi no se modifica el original

            nuevo_historial['raton'].append(movimiento['raton'])  # Agregar nuevo movimiento al historial

            puntuacion = minimax(movimiento, 0, False, nuevo_historial)  # Llamada al algoritmo minimax, y verifica ahi cual es la nueva posicion en vase a los argumentos que tiene.

            if puntuacion > mejor_puntuacion:  # verfica si la puntuación obtenida es mejor que la mejor puntuación actual

                mejor_puntuacion = puntuacion #Actualizar mejor puntuación y movimiento 
                mejor_movimiento = movimiento
        
        # Actualizar posición del ratón y el historial
        self.posicion_raton = mejor_movimiento['raton'] # Establece la nueva posición del ratón al mejor movimiento encontrado.

        self.historial['raton'].append(self.posicion_raton) # Agrega esta nueva posición al historial del ratón.

        self.actualizar_tablero()  # Actualizar el tablero
        
        if es_fin_del_juego({'gato': self.posicion_gato, 'raton': self.posicion_raton}):  # Verificar si el juego terminó
            
            self.mostrar_mensaje_final("¡El gato ha atrapado al ratón!")  # Llamamos al metodo mostrar mensaje si el gato atrapó al ratón

            return
        
        self.turno += 1  # Incrementar el contador de turnos
        self.root.after(500, self.jugar_turno_gato)  # Esperar 500 ms y ejecutar el turno del gato

    def jugar_turno_gato(self):  # Turno del gato

        mejor_puntuacion = float('inf')  # Iniciar mejor puntuación como más infinito

        mejor_movimiento = None

        for movimiento in obtener_todos_los_movimientos_posibles('gato', {'gato': self.posicion_gato, 'raton': self.posicion_raton}, self.historial):

            nuevo_historial = {k: v[:] for k, v in self.historial.items()}  # Copiar el historial

            nuevo_historial['gato'].append(movimiento['gato'])  # Agregar nuevo movimiento al historial

            puntuacion = minimax(movimiento, 0, True, nuevo_historial)  # Llamada al algoritmo minimax

            if puntuacion < mejor_puntuacion:  # Actualiza la mejor puntuación y movimiento

                mejor_puntuacion = puntuacion
                mejor_movimiento = movimiento
        
        # Actualizar posición del gato y el historial
        self.posicion_gato = mejor_movimiento['gato']

        self.historial['gato'].append(self.posicion_gato)

        self.actualizar_tablero()  # Actualizar el tablero
        
        if es_fin_del_juego({'gato': self.posicion_gato, 'raton': self.posicion_raton}):  # Verificar si el juego terminó

            self.mostrar_mensaje_final("¡El gato ha atrapado al ratón!")  # Mostrar mensaje si el gato atrapó al ratón

            return
        
        self.turno += 1  # Incrementar el contador de turnos
        self.root.after(500, self.jugar)  # Esperar 500 ms y ejecutar el turno del ratón

    def mostrar_mensaje_final(self, mensaje):

        # especificamos las coordenadas de donde mismo aparecera el mensaje, el texto del mensaje, la fuente, el color, y la etiqueta del mensaje 
        self.tablero.create_text(250, 250, text=mensaje, font=("Helvetica", 16), fill="black", tags="mensaje_final")  # Mostrar mensaje final en el centro del tablero

# Crear la ventana principal de Tkinter
root = tk.Tk() #llamamos a tkinter en la variable root para enviarlo a la ventana principal
juego = JuegoGatoRaton(root)  # Instanciar el valor de la clase del juego. Le pasamos la ventana principal a la clase y asi dibujar el tablero.

root.mainloop()  # Iniciar el bucle principal de Tkinter. 
