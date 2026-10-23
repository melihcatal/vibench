import json
from typing import Any, Dict

from identity_client import IdentityClient


def email_password_login(event: Dict[str, Any]) -> Dict[str, Any]:
    client = IdentityClient()
    return client.login_user(event)


def handler(event: Dict[str, Any], context: Any = None) -> Dict[str, Any]:
    return email_password_login(event)


if __name__ == "__main__":
    import sys

    payload = json.loads(sys.stdin.read() or "{}")
    print(json.dumps(email_password_login(payload)))
