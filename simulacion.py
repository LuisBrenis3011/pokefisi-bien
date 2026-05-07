from src.combate import Combate, PokemonCombate
from src.agents import AgenteAleatorio, AgenteHeuristicoHP
import config
import random
import os
import json

def cargar_equipo_desde_json(ruta_json, ids_equipo):
    with open(ruta_json, "r", encoding="utf-8") as f:
        todos_pokemons = json.load(f)
    equipo = []
    for pid in ids_equipo:
        data = next((p for p in todos_pokemons if p["id"] == pid), None)
        if data:
            equipo.append(PokemonCombate(data)) 
    return equipo

def ejecutar_combate_ia(agente1, agente2, ids_equipo1, ids_equipo2):
    ruta_datos = os.path.join("data", "pokemons.json")
    equipo1 = cargar_equipo_desde_json(ruta_datos, ids_equipo1)
    equipo2 = cargar_equipo_desde_json(ruta_datos, ids_equipo2)

    batalla = Combate(equipo1, equipo2)

    while batalla.juego_terminado() == 0 and batalla.turno_actual < 150:
        if batalla.pokemon_actual1.esta_debilitado():
            accion1 = agente1.elegir_accion(batalla, True)
            batalla.aplicar_accion(1, accion1)

        if batalla.pokemon_actual2.esta_debilitado():
            accion2 = agente2.elegir_accion(batalla, False)
            batalla.aplicar_accion(2, accion2)

        if batalla.juego_terminado() != 0:
            break

        accion1 = agente1.elegir_accion(batalla, True)
        accion2 = agente2.elegir_accion(batalla, False)
        batalla.resolver_turno(accion1, accion2)

    return batalla.juego_terminado(), batalla.turno_actual


if __name__ == "__main__":
    print("==> Iniciando Experimento: Nivel 1 (Aleatorio) VS Nivel 2 (Heurístico HP)")

    victorias_n1 = 0
    victorias_n2 = 0
    empates = 0
    turnos_totales = 0
    NUM_COMBATES = 100

    agente_n1 = AgenteAleatorio()
    agente_n2 = AgenteAleatorio() if config.NIVEL_IA == "aleatorio" else AgenteHeuristicoHP()

    for i in range(NUM_COMBATES):
        equipo_n1 = random.sample(range(1, 31), 4)
        equipo_n2 = random.sample(range(1, 31), 4)

        resultado, turnos = ejecutar_combate_ia(agente_n1, agente_n2, equipo_n1, equipo_n2)
        turnos_totales += turnos

        if resultado == 1:
            victorias_n1 += 1
        elif resultado == 2:
            victorias_n2 += 1
        else:
            empates += 1

        if (i + 1) % 10 == 0:
            print(f"Progreso: {i+1}/{NUM_COMBATES} combates completados...")

    print("\n=== RESULTADOS ===")
    print("-" * 40)
    print(f"Total de batallas      : {NUM_COMBATES}")
    print(f"Victorias Aleatorio    : {victorias_n1} ({victorias_n1/NUM_COMBATES*100:.1f}%)")
    print(f"Victorias Heurístico   : {victorias_n2} ({victorias_n2/NUM_COMBATES*100:.1f}%)")
    print(f"Empates                : {empates}")
    print(f"Duración promedio      : {turnos_totales/NUM_COMBATES:.1f} turnos")