from __future__ import annotations

import os

from security_client import fetch_secret_value


def main() -> str:
    secret_name = os.environ.get("API_KEY_SECRET_NAME", "api-key")
    return fetch_secret_value(secret_name)


if __name__ == "__main__":
    print(main())
