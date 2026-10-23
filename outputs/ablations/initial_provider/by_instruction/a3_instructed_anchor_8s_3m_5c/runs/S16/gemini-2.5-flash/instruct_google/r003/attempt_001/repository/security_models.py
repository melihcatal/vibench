from dataclasses import dataclass

@dataclass
class SecretRequest:
    project_id: str
    secret_id: str
    version_id: str = "latest"

@dataclass
class SecretResponse:
    secret_id: str
    version_id: str
    payload: str

def normalize_secret_response(secret_id: str, version_id: str, payload: str) -> SecretResponse:
    """Normalizes a secret response into a structured SecretResponse object."""
    return SecretResponse(secret_id=secret_id, version_id=version_id, payload=payload)
