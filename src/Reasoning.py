import numpy as np
from .Simplify import *

def get_intensity(disc_matrix: DiscernibilityMatrix, known_attr: set) -> np.ndarray:
    intensity = disc_matrix.get_intensity_dict()
    temp = []
    for attr in known_attr:
        temp.append(intensity.get(attr))
    return np.array(temp).T

def reasoning_bn(disc_matrix: DiscernibilityMatrix, known_attr: set, prior_prob: np.ndarray) -> np.ndarray:
    mini_set = get_greedy_cover(disc_matrix)
    mini_set = refine_cover(mini_set, disc_matrix)
    print('【最小覆盖集】')
    print(mini_set)
    intensity_plus = get_intensity(disc_matrix, known_attr)
    intensity_minus = 1 - get_intensity(disc_matrix, mini_set - known_attr)
    results = np.cumprod(intensity_plus, axis=1)[:, -1] * np.cumprod(intensity_minus, axis=1)[:, -1] * prior_prob
    return results.round(4)