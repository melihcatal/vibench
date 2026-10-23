from __future__ import annotations

from security_client import AzureKeyVaultSecurityClient, load_security_config
from security_models import ManagedKeyRequest


if __name__ == "__main__":
    client = AzureKeyVaultSecurityClient(load_security_config())
    signed = client.sign(ManagedKeyRequest(key_id=client.config.signing_key_id or client.config.key_name, plaintext="sign me"))
    client.verify(ManagedKeyRequest(key_id=client.config.signing_key_id or client.config.key_name, plaintext="sign me", ciphertext=signed.result["signature"]))
