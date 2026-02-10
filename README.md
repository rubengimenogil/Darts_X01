# Darts_X01

Proyecto de simulación de partidas de dardos X01 (121, 301, 501, 701, 901).

**Resumen**
- **Dards X01:** Simula partidas entre varios jugadores donde cada uno empieza con una puntuación inicial (p. ej. 121) y lanza hasta 3 dardos por ronda para reducir su puntuación a cero.

**Características**
- **Clases principales:** `Jugador`, `Dardo`, `Ronda`, `Partida`, `GameRunner`.
- **Validaciones:** nombres no vacíos, números de dardo entre 1-20, multiplicadores 1-3.
- **Simulación reproducible:** opción de semilla aleatoria para resultados deterministas.
- **Historial detallado:** registro por ronda y por jugador.

**Requisitos**
- Python 3.8+

**Uso rápido**
- Ejecutar la simulación interactiva:

```bash
python Dardos_X01.py
```

- Ejecutar la simulación desde `GameRunner` en código:

```py
from Dardos_X01 import Jugador, GameRunner
players = [Jugador("A"), Jugador("B")]
runner = GameRunner(players, tipo=121)
runner.run(max_rondas=10, semilla=42, verbose=True)
```

**Estructura de código**
- `Jugador`: maneja nombre, puntos e historial; métodos para lanzar dardo y jugar ronda.
- `Dardo`: representa un lanzamiento (número y multiplicador) y calcula puntos.
- `Ronda`: contenedor de hasta 3 `Dardo` y suma de puntos.
- `Partida`: orquesta la partida entre jugadores, lleva historial y determina ganador.
- `GameRunner`: helper/CLI para ejecutar simulaciones y mostrar resultados.

**Licencia**
- Ver [LICENSE.md](LICENSE.md) para los términos de la licencia.
