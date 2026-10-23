from typing import Any, Dict, TypedDict
import json


class ApiKeySecret(TypedDict):
    api_key: str


class DbConnectionSecret(TypedDict):
    host: str
    port: int
    username: str
    password: str


def parse_json_secret(secret_string: str) -> Dict[str, Any]:
    return json.loads(secret_string)
