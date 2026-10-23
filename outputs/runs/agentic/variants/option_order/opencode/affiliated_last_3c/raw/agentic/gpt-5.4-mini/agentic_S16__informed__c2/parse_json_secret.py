from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

from security_client import default_secret_name, secret_vault_url
from security_models import parse_json_payload, normalize_secret_value


def parse_json_secret(secret_name: str = "json-secret"):
    client = SecretClient(
        vault_url=secret_vault_url(), credential=DefaultAzureCredential()
    )
    return parse_json_payload(
        normalize_secret_value(
            client.get_secret(default_secret_name(secret_name)).value
        )
    )
