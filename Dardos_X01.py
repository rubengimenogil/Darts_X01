# Creado por Rubén Gimeno Gil
#Dardos X01

"""
Este módulo simula una partida de dardos del tipo X01 (121, 301,
501, 701, 901) entre varios jugadores. Cada jugador comienza con un
puntaje inicial (según el tipo de partida) y lanza hasta 3 dardos por
ronda para reducir su puntaje a cero. El primer jugador en llegar a
cero o menos puntos gana la partida. El módulo incluye clases para
representar jugadores, dardos, rondas y la partida, así como un
GameRunner para ejecutar la simulación y mostrar los resultados.

El módulo también valida las entradas (nombres no vacíos, números de
dardo entre 1 y 20, multiplicadores válidos) y mantiene un historial
detallado de cada ronda para revisar el desarrollo de la partida.
"""

from __future__ import annotations
import random


# =============================================================================
# Clase: Jugador
# Descripción: Representa a un jugador, su nombre y puntos; métodos de juego.
# =============================================================================

class Jugador:

    # Atributos:
    def __init__(self, nombre: str, puntos_iniciales: int = 121) -> None:

        # Valida nombre y puntos iniciales

        # Valida que el nombre del jugador no sea vacío o nulo, y que los puntos iniciales sean un número positivo. Esto asegura que cada jugador tenga un nombre válido y una puntuación inicial adecuada para la partida.
        if nombre is None or not isinstance(nombre, str) or nombre.strip() == "":
            raise ValueError("El nombre del jugador no puede estar vacío")
        
        # Valida que los puntos iniciales sean un número positivo. Esto asegura que cada jugador comience con una puntuación válida para la partida.
        if puntos_iniciales <= 0:
            raise ValueError("Los puntos iniciales deben ser un número positivo")
        
        # Inicializa atributos
        self.nombre = nombre      
        self.puntos = puntos_iniciales
        self.historial: list[Ronda] = []

    # Método para lanzar un dardo individual:
    def lanzar_dardo(self, numero: int, multiplicador: int = 1) -> tuple[int, int]:
        """Lanza un dardo simple/doble/triple.

        Parámetros:
        - numero: int entre 1 y 20
        - multiplicador: 1 (simple), 2 (doble), 3 (triple)

        Devuelve (puntos_anotados, puntos_restantes).
        """
        
        # Valida número y multiplicador
        if not (1 <= numero <= 20):
            raise ValueError("El número debe estar entre 1 y 20")
        
        if multiplicador not in (1, 2, 3):
            raise ValueError("El multiplicador debe ser 1 (simple), 2 (doble) o 3 (triple)")
        
        # Crear el dardo y calcular puntos
        dardo = Dardo(numero, multiplicador)

        # Resta los puntos anotados al total del jugador
        puntos = dardo.puntos()
        self.puntos -= puntos

        # Devuelve puntos anotados y puntos restantes
        return puntos, self.puntos

    # Método para jugar una ronda completa (hasta 3 dardos):    
    def jugar_ronda(self, dardos: list) -> tuple[int, int, Ronda]:
        """Aplica una ronda (hasta 3 dardos) al jugador.
        Devuelve (puntos_ronda, puntos_restantes, ronda_obj).
        """

        # Crea una ronda y añadir los dardos
        ronda = Ronda()
        # Valida y añade cada dardo a la ronda
        for item in dardos:
            # Si el item es un Dardo, lo añadimos directamente. Si es una tupla, la convertimos a Dardo.
            if isinstance(item, Dardo):
                ronda.añadir_dardo(item)
            # Si es una tupla, valida y convierte a Dardo
            else:
                numero, mult = item
                ronda.añadir_dardo(Dardo(numero, mult))
        # Calcula puntos totales de la ronda y resta al jugador
        total = ronda.puntos_totales()
        self.puntos -= total
        self.historial.append(ronda)
        return total, self.puntos, ronda
    
    # Métodos para obtener información del jugador
    def get_nombre(self) -> str:
        return self.nombre
    
    # Método para obtener puntos restantes
    def get_puntos(self) -> int:
        return self.puntos
    
    # Método para cambiar el nombre del jugador
    def set_nombre(self, nuevo_nombre: str) -> None:
        if nuevo_nombre is None or not isinstance(nuevo_nombre, str) or nuevo_nombre.strip() == "":
            raise ValueError("El nombre del jugador no puede estar vacío")
        self.nombre = nuevo_nombre
        return None
    
    # Representación legible del jugador
    def __repr__(self) -> str:
        return f" Jugador: {self.nombre} (Puntos: {self.puntos})"
    
    # Para imprimir el jugador de forma legible
    def __str__(self) -> str:
        return f" Jugador: {self.nombre} (Puntos: {self.puntos})"
    
# =============================================================================
# Clase: Dardo
# Descripción: Representa un lanzamiento (número 1-20 y multiplicador 1-3).
# =============================================================================

class Dardo:
    """Representa un único lanzamiento de dardo."""

    # Atributos:
    def __init__(self, numero: int, multiplicador: int = 1) -> None:

        # Validar número y multiplicador
        if not (1 <= numero <= 20):
            raise ValueError("El número debe estar entre 1 y 20")
        
        if multiplicador not in (1, 2, 3):
            raise ValueError("El multiplicador debe ser 1, 2 o 3")
        
        # Inicializar atributos

        # Validar que el número del dardo esté entre 1 y 20, y que el multiplicador sea 1 (simple), 2 (doble) o 3 (triple). Esto asegura que cada dardo tenga valores válidos para el juego.
        self.numero = numero

        # Validar que el multiplicador sea 1 (simple), 2 (doble) o 3 (triple). Esto asegura que cada dardo tenga un multiplicador válido para el juego.
        self.multiplicador = multiplicador

    # Método para calcular los puntos anotados por el dardo
    def puntos(self) -> int:
        # El puntaje de un dardo se calcula multiplicando el número por el multiplicador (1, 2 o 3).
        return self.numero * self.multiplicador

    # Representación legible del dardo
    def __repr__(self) -> str:

        # Es útil tener una representación legible del dardo que muestre su número y multiplicador de forma clara (por ejemplo, "S20" para un simple 20, "D5" para un doble 5, "T3" para un triple 3). Esto facilita la comprensión de los dardos lanzados en las rondas.
        tipo = {1: 'S', 2: 'D', 3: 'T'}[self.multiplicador]
        return f"Dardo({tipo}{self.numero})"
    
    # Para imprimir el dardo de forma legible
    def __str__(self) -> str:

        # Es útil tener una representación legible del dardo que muestre su número y multiplicador de forma clara (por ejemplo, "S20" para un simple 20, "D5" para un doble 5, "T3" para un triple 3). Esto facilita la comprensión de los dardos lanzados en las rondas.
        tipo = {1: 'S', 2: 'D', 3: 'T'}[self.multiplicador]
        return f"Dardo({tipo}{self.numero})"
    



# =============================================================================
# Clase: Ronda
# Descripción: Contenedor de hasta 3 dardos y cálculo de puntos por ronda.
# =============================================================================


class Ronda:
    """Una ronda puede contener hasta 3 dardos."""

    # Atributos:
    def __init__(self) -> None:
        # Inicializar la lista de dardos vacía
        self.dardos = []

    # Método para añadir un dardo a la ronda
    def añadir_dardo(self, dardo: Dardo) -> None:
        # Validar que el objeto es un Dardo y que no se excede el límite de 3 dardos por ronda
        if not isinstance(dardo, Dardo):
            raise ValueError("Sólo se pueden añadir objetos de tipo Dardo a la ronda")
        # Validar que no se añadan más de 3 dardos a la ronda
        if len(self.dardos) >= 3:
            raise ValueError("Una ronda sólo puede tener 3 dardos como máximo")
        # Añadir el dardo a la lista de dardos de la ronda
        self.dardos.append(dardo)
        
    # Método para calcular los puntos totales de la ronda sumando los puntos de cada dardo
    def puntos_totales(self) -> int:
        return sum(d.puntos() for d in self.dardos)

    # Representación legible de la ronda
    def __repr__(self) -> str:
        return f"Ronda({self.dardos})"
    
    # Para imprimir la ronda de forma legible
    def __str__(self) -> str:
        return f"Ronda con dardos: {', '.join(str(d) for d in self.dardos)} (Total puntos: {self.puntos_totales()})"


# =============================================================================
# Clase: Partida
# Descripción: Gestiona una partida entre jugadores (tipos: 121, 301, 501, 701, 901).
# =============================================================================

class Partida:
    """Gestiona una partida con varios jugadores y diferentes puntuaciones iniciales."""

    TIPOS_VALIDOS = (121, 301, 501, 701, 901)

    # Atributos:
    def __init__(self, jugadores: list, tipo: int = 121) -> None:
        # Validar tipo de partida y lista de jugadores
        if tipo not in self.TIPOS_VALIDOS:
            raise ValueError(f"Tipo de partida inválido: {tipo}")
        if not jugadores:
            raise ValueError("Se necesita al menos un jugador")
        
        # Inicializa atributos
        self.tipo = tipo

        # Clona referencias a Jugador existentes y resetea puntos al comienzo
        self.jugadores = list(jugadores)

        # Inicializa el ganador y el contador de rondas
        self.ganador = None

        # Inicializa el contador de rondas jugadas a 0, ya que al crear la partida aún no se han jugado rondas.
        self.rondas_jugadas = 0

        # Inicia la partida reseteando puntos de los jugadores
        self.iniciar()

        # Historial detallado: lista de dicts por ronda
        self.historial: list[dict] = []

    # Método para iniciar o resetear la partida
    def iniciar(self) -> None:
        """Inicializa/Resetea la partida poniendo a cada jugador con los puntos iniciales."""

        # Resetea los puntos de cada jugador al tipo de partida (121, 301, etc.)
        for j in self.jugadores:
            # Es necesario resetear los puntos de cada jugador al tipo de partida al iniciar o reiniciar la partida. Esto asegura que cada jugador comience con los puntos correctos para esa partida.
            j.puntos = self.tipo

        # Resetea el ganador y el contador de rondas
        self.ganador = None

        # Resetea el contador de rondas jugadas a 0 al iniciar la partida, ya que no se han jugado rondas aún.
        self.rondas_jugadas = 0


    # Método para jugar una ronda completa para todos los jugadores
    def jugar_ronda(self, dardos_por_jugador: list[list]) -> None:
        """Aplica una ronda: `dardos_por_jugador` es lista paralela con 3 dardos (tuplas o Dardo) por jugador."""

        # Valida que se proporcionen dardos para cada jugador
        if len(dardos_por_jugador) != len(self.jugadores):
            raise ValueError("Debe proporcionar una lista de dardos por cada jugador")
        
        # zip empareja `self.jugadores` con `dardos_por_jugador` elemento a elemento.
        # Si una lista es más corta, zip se detiene (elementos sobrantes se ignoran).
        # Por eso validamos antes que tengan la misma longitud; en Python 3.10+ puedes usar
        # `zip(..., strict=True)` para forzar igualdad de longitudes.

        ronda_num = self.rondas_jugadas + 1
        resumen_ronda = {"ronda": ronda_num, "jugadores": []}

        for jugador, dardos in zip(self.jugadores, dardos_por_jugador):
            # Aunque el enunciado no lo especifica, es necesario validar que se proporcionen dardos para cada jugador en la ronda. Esto asegura que cada jugador tenga la oportunidad de lanzar sus dardos y que la ronda se ejecute correctamente.
            puntos_ronda, puntos_restantes, ronda_obj = jugador.jugar_ronda(dardos)

            resumen_ronda["jugadores"].append({
                "nombre": jugador.nombre,
                "puntos_ronda": puntos_ronda,
                "puntos_restantes": puntos_restantes,
                "dardos": [str(d) for d in ronda_obj.dardos]
            })

            # Aunque el enunciado no lo especifica, es necesario verificar después de cada ronda si algún jugador ha llegado a cero o menos puntos para determinar el ganador de la partida. Esto asegura que la partida termine correctamente cuando un jugador gana.
            if puntos_restantes <= 0:
                self.ganador = jugador
                # Aunque el enunciado no lo especifica, es importante detener la partida inmediatamente cuando se determina un ganador, ya que no tiene sentido seguir jugando rondas adicionales después de que alguien ha ganado. Esto asegura que la partida termine de manera lógica y justa.
                break

        # Incrementa el contador de rondas jugadas después de procesar la ronda completa para todos los jugadores.    
        self.rondas_jugadas += 1
        self.historial.append(resumen_ronda)

    # Método para imprimir el historial de la partida de forma legible
    def imprimir_historial(self) -> None:
        # Es útil tener un método para imprimir el historial de la partida de forma legible, mostrando las rondas jugadas, los dardos lanzados por cada jugador en cada ronda, los puntos anotados en cada ronda y los puntos restantes después de cada ronda. Esto permite revisar el desarrollo de la partida y entender cómo se llegó al resultado final.
        if not self.historial:
            print("No hay historial de la partida.")
            return
        for ronda in self.historial:
            print(f"Ronda {ronda['ronda']}:")
            for partida in ronda["jugadores"]:
                print(f"  {partida['nombre']}: {', '.join(partida['dardos'])} -> {partida['puntos_ronda']} pts (restantes {partida['puntos_restantes']})")
            

    # Método para simular una partida completa con rondas aleatorias

    def simular(self, max_rondas: int = 15, semilla: int | None = None) -> tuple[int, Jugador | None]:
        """Simula rondas aleatorias hasta que haya un ganador o se alcance `max_rondas`.
        Devuelve (rondas_jugadas, ganador o None).
        """

        # Es útil tener un método para simular una partida completa con rondas aleatorias. Esto permite probar la lógica del juego y ver cómo se desarrollan las partidas sin necesidad de ingresar manualmente los dardos. El método simular ejecutará rondas aleatorias hasta que haya un ganador o se alcance un número máximo de rondas para evitar bucles infinitos.

        # Si se proporciona una semilla, se utiliza para generar números aleatorios de manera reproducible. Esto es útil para pruebas y depuración, ya que permite obtener los mismos resultados en cada ejecución.
        if semilla is not None:
            random.seed(semilla)

        # Inicia la partida reseteando puntos de los jugadores antes de simular las rondas.
        self.iniciar()

        # Simular rondas aleatorias hasta que haya un ganador o se alcance el número máximo de rondas.
        for _ in range(max_rondas):
            # Crear una lista de dardos para cada jugador en esta ronda
            dardos_por_jugador = []
            # Para cada jugador, generar una ronda de 3 dardos aleatorios (número entre 1 y 20, multiplicador entre 1 y 3) y almacenarlos en una lista paralela a la lista de jugadores. Luego, llamar al método jugar_ronda con esta lista de dardos para procesar la ronda completa.
            for _ in self.jugadores:
                # generar hasta 3 dardos (aquí siempre 3)
                ronda = []

                # Se generan hasta 3 dardos aleatorios para cada jugador en cada ronda. Esto asegura que cada jugador tenga la oportunidad de lanzar sus dardos y que la ronda se ejecute correctamente con la cantidad adecuada de lanzamientos.
                for __ in range(3):

                    # Se generan números aleatorios para el número del dardo (entre 1 y 20) y para el multiplicador (entre 1 y 3) para cada dardo lanzado por cada jugador en cada ronda. Esto asegura que la simulación de la partida sea variada e impredecible, reflejando la naturaleza aleatoria del juego de dardos.
                    num = random.randint(1, 20)
                    mult = random.randint(1, 3)
                    ronda.append((num, mult))  # tupla aceptada por jugar_ronda

                # Se añaden los dardos generados para cada jugador a la lista de dardos por jugador, que luego se pasa al método jugar_ronda para procesar la ronda completa. Esto asegura que cada jugador tenga su propio conjunto de dardos para cada ronda y que la lógica del juego se ejecute correctamente.
                dardos_por_jugador.append(ronda)

            # Se llama al método jugar_ronda con la lista de dardos generados para cada jugador, lo que procesa la ronda completa y actualiza los puntos de cada jugador.
            self.jugar_ronda(dardos_por_jugador)

            # Se verifica después de cada ronda si hay un ganador. Si se determina un ganador, se detiene la simulación de la partida, ya que no tiene sentido seguir jugando rondas adicionales después de que alguien ha ganado. Esto asegura que la partida termine de manera lógica y justa.
            if self.ganador:
                break

        # Retorna el número de rondas jugadas y el ganador (o None si no hay ganador después de max_rondas). Esto permite obtener un resumen de la simulación de la partida, incluyendo cuántas rondas se jugaron y quién ganó.
        return self.rondas_jugadas, self.ganador

# =============================================================================
# Clase: GameRunner
# Descripción: Clase para ejecutar la simulación de una partida y mostrar resultados.
# =============================================================================


class GameRunner:

    # Atributos:
    def __init__(self, jugadores, tipo=121) -> None:
        # Validar tipo de partida y lista de jugadores
        if tipo not in Partida.TIPOS_VALIDOS:
            raise ValueError(f"Tipo de partida inválido: {tipo}")
        if not jugadores:
            raise ValueError("Se necesita al menos un jugador")
        
        # Inicializar la partida con los jugadores y el tipo de partida especificados. Esto asegura que el GameRunner tenga una instancia de Partida configurada correctamente para ejecutar la simulación.
        self.partida = Partida(jugadores, tipo=tipo)

    # Método para ejecutar la simulación de la partida y mostrar los resultados
    def run(self, max_rondas=10, semilla=None, verbose: bool = False) -> None:
        # Simula la partida utilizando el método simular de la clase Partida, pasando el número máximo de rondas y la semilla para la generación de números aleatorios. Luego, imprime el número de rondas jugadas y el ganador de la partida. Esto permite ejecutar la simulación de manera sencilla y ver los resultados de forma clara.
        rondas, ganador = self.partida.simular(max_rondas=max_rondas, semilla=semilla)
        print(f"Rondas: {rondas}, Ganador: {ganador}")
        if verbose:
            print("\nHistorial detallado:")
            self.partida.imprimir_historial()

    # Input para pedir el tipo de partida al usuario

    @staticmethod
    def pedir_tipo() -> int:
        # Solicita al usuario que ingrese el tipo de partida (121, 301, 501, 701, 901) y valida la entrada. Si la entrada no es válida, muestra un mensaje de error y vuelve a solicitar hasta que se ingrese un tipo válido. Esto asegura que el usuario seleccione un tipo de partida correcto para la simulación.
        while True:
            try:
                tipo = int(input("Tipo de partida (121, 301, 501, 701, 901): "))
                if tipo in Partida.TIPOS_VALIDOS:
                    return tipo
                else:
                    print(f"Tipo inválido. Debe ser uno de: {Partida.TIPOS_VALIDOS}")
            except ValueError:
                print("Entrada no válida. Por favor ingrese un número entero.")

    # Input para pedir el número máximo de rondas al usuario

    @staticmethod
    def pedir_max_rondas() -> int:
        # Solicita al usuario que ingrese el número máximo de rondas para la simulación y valida que sea un número entero positivo. Si la entrada no es válida, muestra un mensaje de error y vuelve a solicitar hasta que se ingrese un número válido. Esto asegura que el usuario configure correctamente el número máximo de rondas para la simulación.
        while True:
            try:
                max_rondas = int(input("Número máximo de rondas (enter = 10): ") or "10")
                if max_rondas > 0:
                    return max_rondas
                else:
                    print("El número de rondas debe ser un entero positivo.")
            except ValueError:
                print("Entrada no válida. Por favor ingrese un número entero positivo.")

    @classmethod

    # Método principal para ejecutar el programa, que solicita al usuario el tipo de partida, el número máximo de rondas y los nombres de los jugadores, luego crea una instancia de GameRunner y ejecuta la simulación. Esto permite iniciar el programa de manera interactiva y configurar la partida según las preferencias del usuario.

    def main(cls, semilla: int | None = 42) -> int:
    # Usamos `semilla=42` para llamar a `random.seed(semilla)` en la simulación.
    # Esto hace la simulación determinista y reproducible (útil para pruebas).
        tipo = cls.pedir_tipo()
        max_rondas = cls.pedir_max_rondas()
        nombres = input("Nombres de jugadores separados por comas (enter = Jugador1, Jugador2): ").strip()

        # Si el usuario no ingresa ningún nombre (solo presiona enter), se crean dos jugadores por defecto con los nombres "Jugador1" y "Jugador2". Esto asegura que siempre haya al menos dos jugadores en la simulación, incluso si el usuario no proporciona nombres personalizados.
        if not nombres:
            jugadores = [Jugador("Jugador1"), Jugador("Jugador2")]

        # Si el usuario ingresa nombres separados por comas, se crean instancias de Jugador para cada nombre ingresado, asegurándose de que no haya nombres vacíos o solo espacios. Esto permite al usuario personalizar los nombres de los jugadores en la simulación.
        else:
            jugadores = [Jugador(n.strip()) for n in nombres.split(",") if n.strip()]
            if not jugadores:
                raise ValueError("Debe ingresar al menos un nombre de jugador.")
        
        # Se solicita al usuario si desea mostrar el historial detallado de la partida. Si el usuario ingresa "s" (sí), se establece la variable `verbose` en True, lo que permitirá mostrar el historial detallado al finalizar la simulación. Si el usuario ingresa "n" (no) o simplemente presiona enter, `verbose` se establece en False y no se mostrará el historial detallado. Esto permite al usuario elegir si desea ver un resumen simple de la partida o un desglose completo de cada ronda y los dardos lanzados por cada jugador.    
        mostrar = input("¿Mostrar historial detallado? (s/n, enter = n): ").strip().lower()
        verbose = mostrar == "s"

        # Se crea una instancia de GameRunner con la lista de jugadores y el tipo de partida especificados.
        runner = cls(jugadores, tipo=tipo)

        # Se ejecuta la simulación de la partida utilizando el método run, pasando el número máximo de rondas y la semilla para la generación de números aleatorios. Esto inicia la simulación y muestra los resultados al usuario.
        runner.run(max_rondas=max_rondas, semilla=semilla, verbose=verbose)

        # El método main no necesita retornar ningún valor, ya que su función principal es ejecutar la simulación y mostrar los resultados. Por lo tanto, se puede retornar None o simplemente no incluir una declaración de retorno, lo que en Python implica retornar None por defecto.
        return 0


# Punto de entrada del programa
if __name__ == "__main__":

    # Se llama al método main de la clase GameRunner para iniciar el programa. Esto permite que el programa se ejecute de manera interactiva cuando se ejecuta directamente, solicitando al usuario la configuración de la partida y mostrando los resultados de la simulación.
    GameRunner.main()
