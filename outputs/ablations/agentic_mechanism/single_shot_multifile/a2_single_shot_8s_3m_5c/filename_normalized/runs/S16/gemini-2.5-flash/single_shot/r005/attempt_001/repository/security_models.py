import json

class SecretValue:
    def __init__(self, secret_string: str):
        self._secret_string = secret_string

    def get_string(self) -> str:
        return self._secret_string

    def get_json(self) -> dict:
        return json.loads(self._secret_string)
