import json
from typing import Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class Secret:
    name: str
    value: str
    version_id: Optional[str] = None


def parse_json_secret(value: str) -> Dict[str, Any]:
    return json.loads(value)


def parse_db_secret(value: str) -> Dict[str, Any]:
    return parse_json_secret(value)
