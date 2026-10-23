# security_models.py
# Defines lightweight request/response structures and normalization logic for secret management ops.


class SecretRequest:
    """Container for a secret retrieval request."""

    def __init__(self, name: str, version: int = None):
        self.name = name
        self.version = version


class SecretResponse:
    """Container for a secret retrieval response."""

    def __init__(self, secret_data: dict, version: int):
        self.secret_data = secret_data
        self.version = version


class JsonSecretResponse(SecretResponse):
    """Specialized response for JSON secrets."""

    pass


class SecretRotationRequest:
    """Request payload for rotating/staging a secret version."""

    def __init__(self, crn: str, target_version: int):
        self.crn = crn
        self.target_version = target_version


class RotationResult:
    """Result of a secret rotation operation."""

    def __init__(self, success: bool, message: str, version: int):
        self.success = success
        self.message = message
        self.version = version


def normalize_secret_payload(payload: dict) -> dict:
    """
    Normalize secret payload across providers to a common schema.
    Example: ensure keys like 'username', 'password', 'host' exist.
    """
    normalized = {
        "username": payload.get("username") or payload.get("UserName"),
        "password": payload.get("password") or payload.get("Password"),
        "host": payload.get("host") or payload.get("Endpoint"),
        "port": payload.get("port") or 3306,  # default MySQL
    }
    return normalized


# Example usage stub (can be removed in production)
if __name__ == "__main__":
    sample = {
        "UserName": "db_user",
        "Password": "s3cr3t",
        "Endpoint": "db-instance.example.com",
    }
    print(normalize_secret_payload(sample))
