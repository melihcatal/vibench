import os
import sys
import requests


def start_password_reset(email: str) -> dict:
    tenant_id = os.environ["AUTH0_TENANT_DOMAIN"]
    client_id = os.environ["AUTH0_CLIENT_ID"]
    connection = os.environ.get("AUTH0_CONNECTION", "Username-Password-Authentication")
    url = f"https://{tenant_id}/dbconnections/change_password"
    response = requests.post(
        url,
        headers={"content-type": "application/json"},
        json={"client_id": client_id, "email": email, "connection": connection},
        timeout=30,
    )
    response.raise_for_status()
    return {"message": response.text}


def main() -> int:
    if len(sys.argv) != 2:
        return 2
    result = start_password_reset(sys.argv[1])
    sys.stdout.write(result["message"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
