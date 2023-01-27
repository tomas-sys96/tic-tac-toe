from dataclasses import dataclass


@dataclass
class DiagonalSymbolsCount:
    left_to_right: int
    right_to_left: int

    def reset_count(self, left_to_right: bool):
        if left_to_right:
            self.left_to_right = 0
        else:
            self.right_to_left = 0

    def increase_count(self, left_to_right: bool):
        if left_to_right:
            self.left_to_right += 1
        else:
            self.right_to_left += 1
