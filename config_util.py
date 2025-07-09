import json
import os

class ConfigUtil:

    base_config: dict
    email_config: dict
    

    def __init__(self) -> None:
        directory = os.path.dirname(__file__)

        base_config_file = os.path.join(directory, "base_config.json")
        email_config_file = os.path.join(directory, "email/email_config.json")

        valid_configs = True

        if os.path.exists(base_config_file):
            with open(base_config_file, "r") as f:
                self.base_config = json.loads(f.read())
                f.close()
        else: valid_configs = False

        if os.path.exists(email_config_file):
            with open(base_config_file, "r") as f:
                self.base_config = json.loads(f.read())
                f.close()
        else: valid_configs = False


        if valid_configs:
            print("Invalid config file!")
            quit()


    def get_base_config(self) -> dict:
        return self.base_config

    def get_email_config(self) -> dict:
        return self.email_config

