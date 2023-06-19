from math import sqrt

from dataclasses import dataclass
from typing import Tuple


__all__ = ['Point']


@dataclass
class Point:
    x: float
    y: float

    @property
    def tuple(self) -> Tuple[float, float]:
        return self.x, self.y

    def __repr__(self) -> str:
        return f'({self.x} {self.y})'

    def __sub__(self, other) -> float:
        return sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

