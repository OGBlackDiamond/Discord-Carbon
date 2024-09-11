import json
import os

class ConfigUtil:

    config: dict

    def __init__(self) -> None:
        directory = os.path.dirname(__file__).removesuffix("/util")

        config_file = os.path.join(directory, "config.json")

        if os.path.exists(config_file):
            with open(config_file, "r") as f:
                self.config = json.loads(f.read())
                f.close()
                return

        print("Invalid config file!")
        quit()


    def get_config(self) -> dict:
        return self.config

