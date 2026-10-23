from typing import Dict


def parse_secret_response(response: Dict) -> str:
    return response["SecretString"]
