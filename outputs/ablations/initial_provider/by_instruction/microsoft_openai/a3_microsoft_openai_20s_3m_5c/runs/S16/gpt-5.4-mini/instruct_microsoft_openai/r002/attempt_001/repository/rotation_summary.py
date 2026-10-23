from security_client import create_secret_client


def rotation_summary(secret_name: str) -> str:
    client = create_secret_client()
    secret = client.get_secret(secret_name)
    version = getattr(secret.properties, "version", "")
    enabled = getattr(secret.properties, "enabled", None)
    return f"{secret_name}:{version}:{enabled}"
