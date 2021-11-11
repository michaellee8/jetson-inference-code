import time
from enum import IntEnum
from typing import List

def current_milli_time() -> int:
    return round(time.time() * 1000)

class Side(IntEnum):
    NONE = 0
    LEFT = -1
    RIGHT = 1

def times_list(l: List[float], co: float) -> List[float]:
    return [ele * co for ele in l]

def sum_list(*lists: List[float]) -> List[float]:
    return [sum(n) for n in zip(*lists)]