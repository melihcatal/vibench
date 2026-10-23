from typing import Dict


class SecretRequest:
    def __init__(self, secret_name: str):
        self.secret_name = secret_name


class SecretResponse:
    def __init__(self, secret_value: str):
        self.secret_value = secret_value


def normalize_secret_response(response: Dict) -> SecretResponse:
    return SecretResponse(response["value"])
