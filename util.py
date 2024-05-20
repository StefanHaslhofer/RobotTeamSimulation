from typing import Tuple
import numpy as np


def normalize_vec(vec: Tuple) -> Tuple:
    norm = np.linalg.norm(vec)
    if norm == 0:
        return vec
    return tuple(vec / norm)


def add_vec(v1: Tuple, v2: Tuple) -> Tuple:
    return tuple([v1[i] + v2[i] for i in range(len(v1))])
