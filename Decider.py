import random

class Decider:

    @staticmethod
    def choose_options(message: str) -> str:
        choices = message.split(",")
        weights = [1 / len(choices)] * len(choices)
        decision = random.choices(choices, weights=weights, k=1)
        return f"The decision is {decision[0].strip()}"

    @staticmethod
    def coin_flip() -> str:
        choices = ['heads', 'tails']
        weights = [1 / len(choices)] * len(choices)
        decision = random.choices(choices, weights=weights, k=1)
        return decision[0]

    @staticmethod
    def generate_rand_int(start, stop) -> str:
        rand_int = random.randint(start, stop)
        return f"The random number is: {rand_int}"
        