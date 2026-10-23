import json
from security_models import SecretMeta, SecretResponse


def summarize_rotation(secret_name: str) -> str:
    """Summarizes the latest secret rotation status.
    Reads the secret (latest version) and returns a concise human‑readable summary.
    """
    from security_client import SecretClientWrapper

    client = SecretClientWrapper()
    resp = client.get_secret(secret_name)
    # Simple placeholder summary – real implementation could inspect rotation flags
    summary = f'Secret "{secret_name}" is at version {client._detect_provider()} and was last updated on "{resp["meta"]["updated_at"]}".'
    return summary
