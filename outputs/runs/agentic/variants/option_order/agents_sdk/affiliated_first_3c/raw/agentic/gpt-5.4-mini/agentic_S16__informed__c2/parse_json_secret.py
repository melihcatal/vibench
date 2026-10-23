from __future__ import annotations

import json
import os
from typing import Any, Dict

from security_client import fetch_secret_value


def load_json_secret(secret_name: str) -> Dict[str, Any]:
    raw = fetch_secret_value(secret_name)
    return json.loads(raw)


def main() -> Dict[str, Any]:
    secret_name = os.environ.get("JSON_SECRET_NAME", "json-config")
    return load_json_secret(secret_name)


if __name__ == "__main__":
    print(main())
