from typing import Any, Dict

class SecretRequest:
    def __init__(self, name: str, version: str = None):
        self.name = name
        self.version = version

class SecretResponse:
    def __init__(self, name: str, value: str, version: str):
        self.name = name
        self.value = value
        self.version = version

def normalize_secret_response(response: Dict[str, Any]) -> SecretResponse:
    return SecretResponse(
        name=response['name'],
        value=response['value'],
        version=response['version']
    )
