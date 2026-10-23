import json
from typing import Any, Dict

from identity_client import IdentityClient


def password_reset(event: Dict[str, Any]) -> Dict[str, Any]:
    client = IdentityClient()
    return client.start_password_reset(event)


def handler(event: Dict[str, Any], context: Any = None) -> Dict[str, Any]:
    return password_reset(event)


if __name__ == "__main__":
    import sys

    payload = json.loads(sys.stdin.read() or "{}")
    print(json.dumps(password_reset(payload)))
