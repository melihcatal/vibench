from security_client import SecurityClient
from security_models import Secret

def rotate_secret_version(secret_name: str, new_secret_value: str, content_type: str = "text/plain", tags: dict = None) -> Secret:
    client = SecurityClient()
    # For rotation, we typically set a new secret, which creates a new version
    new_secret = Secret(
        name=secret_name,
        value=new_secret_value,
        content_type=content_type,
        tags=tags
    )
    updated_secret = client.set_secret(new_secret)
    return updated_secret

def get_specific_secret_version(secret_name: str, version: str) -> Secret:
    client = SecurityClient()
    secret = client.get_secret_with_version(secret_name, version)
    return secret
