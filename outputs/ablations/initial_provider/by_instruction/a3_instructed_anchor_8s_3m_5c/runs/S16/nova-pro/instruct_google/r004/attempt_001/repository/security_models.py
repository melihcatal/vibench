from typing import Any, Dict

class SecretResponse:
    def __init__(self, data: str):
        self.data = data

    @staticmethod
    def from_payload(payload: Dict[str, Any]) -> 'SecretResponse':
        return SecretResponse(payload['data'].decode('UTF-8'))