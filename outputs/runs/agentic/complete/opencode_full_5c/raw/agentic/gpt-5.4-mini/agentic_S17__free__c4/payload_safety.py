from security_client import SecurityClient


def payload_safety(text: str) -> dict:
    client = SecurityClient()
    unsafe = any(
        token in text.lower() for token in ("password", "secret", "token", "credential")
    )
    return {
        "provider": client.provider,
        "key_id": client.managed_key_id(),
        "unsafe": unsafe,
    }
