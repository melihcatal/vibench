# decrypt_payload.py
# Provider: HashiCorp Vault (via hvac SDK)
# Expected env vars: VAULT_ADDR, VAULT_TOKEN

import os
import hvac
from cryptography.fernet import Fernet


def get_vault_client() -> hvac.Client:
    client = hvac.Client()
    return client


vault = get_vault_client()
kv_secret = vault.secrets.kv.v2.read_secret_version(path="secret/encryption_key")
fernet_key_b64 = kv_secret["data"]["data"]["value"]
fernet_key = Fernet._decode_key(fernet_key_b64)
fernet = Fernet(fernet_key)


def decrypt_payload(ciphertext: str) -> str:
    """Decrypt ciphertext using the Vault‑managed key."""
    return fernet.decrypt(ciphertext.encode()).decode()


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: decrypt_payload.py <ciphertext>", file=sys.stderr)
        sys.exit(1)
    ciphertext = sys.argv[1]
    plaintext = decrypt_payload(ciphertext)
    print(plaintext)
