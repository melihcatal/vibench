from typing import Dict


def normalize_secret_response(response: Dict) -> Dict:
    return {"SecretString": response["SecretString"]}
