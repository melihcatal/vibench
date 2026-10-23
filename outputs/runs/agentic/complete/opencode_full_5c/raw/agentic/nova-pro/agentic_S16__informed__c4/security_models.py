from typing import Any, Dict


def parse_secret_response(response: Dict[str, Any]) -> str:
    return response["secret_data"]
