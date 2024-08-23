import random
from collections import defaultdict

class Randomizer:
    @staticmethod
    def get_random_values():
        signal_model1 = {
            "G-1": "src/main/res/modelo1/G-1.csv",
            "G-2": "src/main/res/modelo1/G-2.csv",
            "A-60x60": "src/main/res/modelo1/A-60x60-1.csv"
        }

        signal_model2 = {
            "g-30x30-1": "src/main/res/modelo2/g-30x30-1.csv",
            "g-30x30-2": "src/main/res/modelo2/g-30x30-2.csv",
            "A-30x30-1": "src/main/res/modelo2/A-30x30-1.csv"
        }

        random_model = random.randint(1, 2)
        signal_gain = random.randint(1, 2)
        algorithm = random.randint(1, 2)
        client_id = random.randint(0, 999)

        if random_model == 1:
            random_signal = random.choice(list(signal_model1.values()))
            selected_model = "src/main/res/modelo1/H-1.csv"
        else:
            random_signal = random.choice(list(signal_model2.values()))
            selected_model = "src/main/res/modelo2/H-2.csv"

        if algorithm == 1:
            selected_algorithm = "CGNE"
        else:
            selected_algorithm = "CGNR"

        selected_variables = {
            "selectedAlgorithm": selected_algorithm,
            "signalGain": signal_gain,
            "selectedSignalPath": random_signal,
            "selectedModelPath": selected_model,
            "selectedModelFlag": random_model,
            "clientId": client_id
        }

        return selected_variables