# encrypt_payload.py
# Provider: HashiCorp Vault (via hvac SDK)
# Expected env vars: VAULT_ADDR, VAULT_TOKEN

import os
import hvac
from cryptography.fernet import Fernet


def get_vault_client() -> hvac.Client:
    """Initialize and return a Vault client using env credentials."""
    client = hvac.Client()
    # Automatically picks up VAULT_ADDR and VAULT_TOKEN
    client.secrets.kv.v2.read_secret_version(path="secret/encryption_key")
    return client


vault = get_vault_client()

# Load the Fernet key stored in Vault under "secret/encryption_key"
kv_secret = vault.secrets.kv.v2.read_secret_version(path="secret/encryption_key")
fernet_key_b64 = kv_secret["data"]["data"]["value"]
fernet_key = Fernet._decode_key(fernet_key_b64)
fernet = Fernet(fernet_key)


def encrypt_payload(plaintext: str) -> str:
    """Encrypt a plaintext string using the Vault‑managed key."""
    return fernet.encrypt(plaintext.encode()).decode()


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: encrypt_payload.py <plaintext>", file=sys.stderr)
        sys.exit(1)
    plaintext = sys.argv[1]
    ciphertext = encrypt_payload(plaintext)
    print(ciphertext)
