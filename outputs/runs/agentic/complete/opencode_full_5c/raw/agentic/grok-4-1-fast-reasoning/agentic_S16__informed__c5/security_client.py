import os
import json
from typing import Dict, Any
from security_models import FetchedSecret


def parse_json_secret(raw_value: str) -> Dict[str, Any]:
    return json.loads(raw_value)


def build_fetched_secret(value: Any, metadata: Dict[str, Any] = None) -> FetchedSecret:
    return {"value": value, "metadata": metadata or {}}
