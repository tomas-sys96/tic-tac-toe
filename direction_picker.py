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

    def get_viable_position(self, symbols_data: dict):
        try:
            # Pick a random viable direction in which to place a symbol
            self.choose_symbol(symbols_data)
            self.choose_direction()
        except IndexError:
            # If there are no viable directions for the chosen symbol, loop through all the symbols
            self._loop_for_viable_position(symbols_data)
        # row_number, column_number = self._get_next_position(game, self.chosen_symbol, self.chosen_direction)

    def _loop_for_viable_position(self, symbols_data: dict):
        for symbol in symbols_data:
            self.chosen_symbol = symbol
            try:
                self.choose_direction()
            except IndexError:
                # If no viable directions yet, try another symbol
                continue
            else:
                # If there's a symbol with at least one viable direction, skip the rest of the loop
                return
