import os
import base64
import json
from typing import Dict, Any


def get_env(key: str, default: str = "") -> str:
    return os.getenv(key, default)


def encode_base64(data: bytes) -> str:
    return base64.b64encode(data).decode("utf-8")


def parse_json_response(content: str) -> Dict[str, Any]:
    return json.loads(content)
