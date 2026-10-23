from typing import Any

class SecretResponse:
    def __init__(self, value: str):
        self.value = value

    @staticmethod
    def from_dict(data: Any) -> 'SecretResponse':
        return SecretResponse(value=data['value'])