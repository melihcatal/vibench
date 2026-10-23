from __future__ import annotations

from security_client import AzureKeyVaultSecurityClient, load_security_config
from security_models import ManagedKeyRequest


if __name__ == "__main__":
    client = AzureKeyVaultSecurityClient(load_security_config())
    client.envelope_encrypt(ManagedKeyRequest(key_id=client.config.key_name, plaintext="envelope payload"))
