from __future__ import annotations

import os

from security_client import fetch_secret
from security_models import SecretRequest


def main() -> str:
    secret_name = os.environ.get("DB_SECRET_NAME", "database-connection")
    request = SecretRequest(secret_name=secret_name)
    return fetch_secret(request).value


if __name__ == "__main__":
    print(main())
