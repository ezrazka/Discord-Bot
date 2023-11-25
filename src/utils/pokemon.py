import json
import random


def get_random_encounter():
    with open('src/data/json/pokemon.json', 'r') as f:
        pokemon_data = json.load(f)

    weights = {
        1: 4,
        2: 3,
        3: 2
    }

    if random.randint(1, 125) <= 1:
        pokemon_names = [
            name for name, data in pokemon_data.items()
            if data["is_legendary"] or data["is_mythical"]
        ]
    else:
        pokemon_names = [
            name for name, data in pokemon_data.items()
            if not data.get("is_legendary") and not data.get("is_mythical")
        ]

    pokemon_weights = [
        weights[pokemon_data[pokemon_name]["evolution-stage"]] for pokemon_name in pokemon_names
    ]
    random_pokemon = random.choices(
        pokemon_names,
        weights=pokemon_weights,
        k=1
    )[0]
    return random_pokemon
