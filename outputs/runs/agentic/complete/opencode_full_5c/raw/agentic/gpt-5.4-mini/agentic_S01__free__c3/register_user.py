import json
from typing import Any, Dict

from identity_client import IdentityClient


def register_user(event: Dict[str, Any]) -> Dict[str, Any]:
    client = IdentityClient()
    return client.register_user(event)


def handler(event: Dict[str, Any], context: Any = None) -> Dict[str, Any]:
    return register_user(event)


if __name__ == "__main__":
    import sys

    payload = json.loads(sys.stdin.read() or "{}")
    print(json.dumps(register_user(payload)))
