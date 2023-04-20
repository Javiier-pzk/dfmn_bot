import random

class Decider:

    @staticmethod
    def choose_options(message: str) -> str:
        choice_str = message[7:].strip()
        if not choice_str:
            return "Please provide at least 1 option, or multiple options separated by commas"
        choices = choice_str.split(",")
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
    def generate_rand_int(message) -> str:
        num_str = message[7:].strip()
        if not num_str:
            return "Please provide a range separated by commas. Eg: 1, 100"
        num_range = num_str.split(",")
        start = int(num_range[0].strip())
        end = int(num_range[-1].strip())
        return str(random.randint(start, end))
        