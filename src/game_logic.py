from pokemones import Pokemon  # solo para la pantalla de selección (main.py)

from combate import (
    PokemonCombate,
    Combate,
    Movimiento,
    cargar_equipos_desde_json,
    guardar_equipos_en_json,
    obtener_efectividad,
    EFECTIVIDAD_TIPOS,
    TIPOS,
)

Pokemon = PokemonCombate