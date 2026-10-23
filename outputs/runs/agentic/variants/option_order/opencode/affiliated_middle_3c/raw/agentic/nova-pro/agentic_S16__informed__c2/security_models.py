from typing import Any, Dict


def normalize_secret_response(response: Dict[str, Any]) -> str:
    return response["SecretString"]


def parse_json_secret(secret_string: str) -> Dict[str, Any]:
    return json.loads(secret_string)
