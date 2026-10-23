import os

from identity_client import IdentityClient, build_identity_payload


def register_user(email: str, password: str, locale: str = "en"):
    client = IdentityClient.from_env()
    payload = build_identity_payload(email, password, locale)
    return client.post("/responses", {"model": "gpt-5.4-mini", "input": [payload]})


if __name__ == "__main__":
    register_user(os.environ.get("ACCOUNT_EMAIL", ""), os.environ.get("ACCOUNT_PASSWORD", ""))
