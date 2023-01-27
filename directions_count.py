from dataclasses import dataclass


@dataclass
class DirectionsCount:
    row_symbols_count: int
    column_symbols_count: int
    left_to_right_diag_symbols_count: int
    right_to_left_diag_symbols_count: int
