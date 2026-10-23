
class SecretRequest:
    def __init__(self, key: str, value: str = None):
        self.key = key
        self.value = value

class SecretResponse:
    def __init__(self, key: str, value: str, version: int):
        self.key = key
        self.value = value
        self.version = version

def normalize_secret_key(key: str) -> str:
    """Normalizes a secret key to a consistent format."""
    return key.strip().lower().replace(' ', '_')

def denormalize_secret_key(normalized_key: str) -> str:
    """Denormalizes a secret key back to a more readable format."""
    return normalized_key.replace('_', ' ').title()
