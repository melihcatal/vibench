import json
from typing import Any, Dict

from identity_client import IdentityClient


def refresh_session(event: Dict[str, Any]) -> Dict[str, Any]:
    client = IdentityClient()
    return client.refresh_session(event.get("refresh_token", ""))


def handler(event: Dict[str, Any], context: Any = None) -> Dict[str, Any]:
    return refresh_session(event)


if __name__ == "__main__":
    import sys

    payload = json.loads(sys.stdin.read() or "{}")
    print(json.dumps(refresh_session(payload)))
