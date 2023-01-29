import random
from dataclasses import dataclass


@dataclass
class DirectionPicker:
    chosen_symbol: dict
    chosen_direction: str

    def choose_symbol(self, symbols_data: dict):
        random_key = random.choice(list(symbols_data.keys()))
        self.chosen_symbol = symbols_data[random_key]

    def choose_direction(self):
        viable_directions = []
        for direction_name, direction_value in self.chosen_symbol["count"].items():
            if direction_value != 0:
                viable_directions.append(direction_name)
        self.chosen_direction = random.choice(viable_directions)
