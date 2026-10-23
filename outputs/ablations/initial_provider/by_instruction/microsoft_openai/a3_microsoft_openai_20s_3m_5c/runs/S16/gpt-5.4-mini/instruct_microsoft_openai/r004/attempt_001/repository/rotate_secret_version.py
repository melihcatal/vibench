import os

from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient


def rotate_secret_version():
    vault_url = os.environ["AZURE_KEY_VAULT_URL"]
    secret_name = os.getenv("ROTATE_SECRET_NAME", "rotating-secret")
    version = os.getenv("SECRET_VERSION")
    stage = os.getenv("SECRET_STAGE")
    client = SecretClient(vault_url=vault_url, credential=DefaultAzureCredential())
    if version:
        return client.get_secret(secret_name, version=version).value
    if stage:
        return client.get_secret(secret_name).value
    return client.get_secret(secret_name).value
