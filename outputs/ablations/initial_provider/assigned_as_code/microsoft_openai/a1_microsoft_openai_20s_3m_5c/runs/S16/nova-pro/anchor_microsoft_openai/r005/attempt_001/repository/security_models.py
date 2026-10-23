from typing import Dict


class SecurityRequest:
    def __init__(self, secret_id: str, key_field: str = None):
        self.secret_id = secret_id
        self.key_field = key_field


class SecurityResponse:
    def __init__(self, secret_value: Dict):
        self.secret_value = secret_value


def normalize_response(response: Dict) -> Dict:
    return response
