from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

from security_client import default_secret_name, secret_vault_url
from security_models import normalize_secret_value


def rotate_secret_version(
    secret_name: str = "rotating-secret",
    version: str | None = None,
    stage: str | None = None,
):
    client = SecretClient(
        vault_url=secret_vault_url(), credential=DefaultAzureCredential()
    )
    secret = (
        client.get_secret(default_secret_name(secret_name), version=version)
        if version
        else client.get_secret(default_secret_name(secret_name))
    )
    if (
        stage
        and getattr(secret, "properties", None)
        and getattr(secret.properties, "tags", None)
    ):
        if secret.properties.tags.get("stage") != stage:
            return None
    return normalize_secret_value(secret.value)
