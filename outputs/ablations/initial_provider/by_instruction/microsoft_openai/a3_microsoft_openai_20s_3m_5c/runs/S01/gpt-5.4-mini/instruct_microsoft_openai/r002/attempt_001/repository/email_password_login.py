from identity_client import IdentityClient, build_identity_payload


def email_password_login(email: str, password: str, locale: str = "en"):
    client = IdentityClient.from_env()
    payload = build_identity_payload(email, password, locale)
    return client.post("/chat/completions", {"model": "gpt-5.4-mini", "messages": [payload]})
