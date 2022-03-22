from random import randint
from random import seed


def generate_random_number(range1, range2):
    seed()
    return randint(range1, range2)
