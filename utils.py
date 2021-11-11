import time
from enum import Enum

def current_milli_time() -> int:
    return round(time.time() * 1000)

class Side(Enum):
    NONE: int = 0
    LEFT: int = -1
    RIGHT: int = 1