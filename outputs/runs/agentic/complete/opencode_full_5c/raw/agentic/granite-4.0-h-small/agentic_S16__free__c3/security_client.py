import os
import json


class SecretManagementClient:
    """Local helper client for interacting with a managed secret store.

    The class abstracts the underlying provider so the same-scenario files can swap
    providers without touching integration logic.
    """

    def __init__(self):
        # Example: configure provider credentials via environment variables
        self.provider = os.getenv("SECRET_PROVIDER", "HASHI_VAULT")
        if self.provider == "AWS_SM":
            from aws_secretsmanager import SecretsManagerClient

            self.client = SecretsManagerClient()
        elif self.provider == "AZURE_KV":
            from azure_keyvault import KeyVaultClient

            self.client = KeyVaultClient()
        else:  # default to HashiCorp Vault
            from vault_client import VaultClient

            self.client = VaultClient()

    def get_secret(self, name):
        """Retrieve the default version of a secret."""
        return self.client.read(name)

    def get_secret_version(self, name, version):
        """Retrieve a specific version (or 'staged') of a secret."""
        return self.client.read_version(name, version)
