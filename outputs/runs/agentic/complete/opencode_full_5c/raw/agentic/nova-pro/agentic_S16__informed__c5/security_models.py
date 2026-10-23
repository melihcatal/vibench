from typing import Any, Dict


class SecretResponse:
    def __init__(self, secret_string: str):
        self.secret_string = secret_string

    def to_dict(self) -> Dict[str, Any]:
        return {"secret_string": self.secret_string}
