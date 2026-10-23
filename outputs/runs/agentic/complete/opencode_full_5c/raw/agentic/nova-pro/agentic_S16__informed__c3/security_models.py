from typing import Any, Dict


def normalize_secret_response(response: Dict[str, Any]) -> Dict[str, Any]:
    return {"SecretString": response["SecretString"]}
