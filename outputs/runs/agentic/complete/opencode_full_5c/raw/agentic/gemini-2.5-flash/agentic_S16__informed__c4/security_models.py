import json
from typing import Dict, Any


class SecretData:
    def __init__(self, secret_string: str):
        self.secret_string = secret_string

    def to_json(self) -> Dict[str, Any]:
        try:
            return json.loads(self.secret_string)
        except json.JSONDecodeError:
            return {"raw_secret": self.secret_string}
