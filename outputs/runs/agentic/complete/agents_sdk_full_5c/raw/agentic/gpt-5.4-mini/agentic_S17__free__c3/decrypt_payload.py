from __future__ import annotations

from security_client import AzureKeyVaultSecurityClient, load_security_config
from security_models import ManagedKeyRequest


if __name__ == "__main__":
    client = AzureKeyVaultSecurityClient(load_security_config())
    ciphertext = client.encrypt(ManagedKeyRequest(key_id=client.config.key_name, plaintext="managed decryption payload")).result["ciphertext"]
    client.decrypt(ManagedKeyRequest(key_id=client.config.key_name, ciphertext=ciphertext))
