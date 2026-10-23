from typing import Dict


class SecretResponse:
    def __init__(self, secret_string: str):
        self.secret_string = secret_string

    def to_dict(self) -> Dict:
        return {"SecretString": self.secret_string}
