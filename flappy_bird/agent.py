import random
from bird import Bird

class Agent:
    def __init__(self, bird: Bird) -> None:
        self.__bird = bird

        random.random()