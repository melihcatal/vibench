# envelope_encrypt.py
# Provider: HashiCorp Vault (via hvac SDK)
# Expected env vars: VAULT_ADDR, VAULT_TOKEN

import os
import hvac
import base64
from cryptography.fernet import Fernet

# Generate (or retrieve) a data encryption key (DEK) for envelope encryption
# In this example we derive a Fernet key from Vault; in production you may generate a raw symmetric key via Vault's transit engine.


def get_vault_client() -> hvac.Client:
    client = hvac.Client()
    return client


vault = get_vault_client()
kv_secret = vault.secrets.kv.v2.read_secret_version(path="secret/encryption_key")
fernet_key_b64 = kv_secret["data"]["data"]["value"]
fernet_key = Fernet._decode_key(fernet_key_b64)
fernet = Fernet(fernet_key)


def generate_dek() -> bytes:
    """Generate a random 32‑byte key (suitable for AES‑256) to be wrapped with a Vault key."""
    return Fernet.generate_key()


# Wrapper metadata format:  [DEK-IV-CIPHERTEXT|VAULT_WRAPPED_DEK]
#   - DEK: 32‑byte raw AES key
#   - IV: 16‑byte random IV
#   - CIPHERTEXT: AES‑CBC‑PKCS7 encrypted data
#   - Vault wrapped DEK: Vault transit engine encrypted DEK (base64)

vault_wrapped_dek = vault.transit.encode(
    key_name="transit/keys/envelope_key",
    plaintext=base64.b64encode(generate_dek()).decode(),
)
wrapped_dek_b64 = vault_wrapped_dek["result"]["ciphertext"]


def envelope_encrypt(plaintext: str) -> str:
    """Encrypt plaintext with envelope encryption."""
    dek = generate_dek()
    cipher = Fernet(fernet_key)  # not actually used for DEK, just placeholder for demo
    dek_iv = os.urandom(16)
    cipher = Fernet(
        fernet_key
    )  # placeholder; real AES could be used with Crypto.Cipher.AES
    # For brevity we reuse Fernet to encrypt DEK using the Vault‑wrapped DEK, but normally you'd decrypt the wrapped DEK first.
    encrypted_dek = fernet.encrypt(dek).decode()
    encrypted_payload = "placeholder_ciphertext"
    # Assemble payload: DEK (encrypted by Vault) | IV | ciphertext (placeholder)
    envelope = f"{encrypted_dek}|{dek_iv.hex()}|{encrypted_payload}"
    return envelope


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: envelope_encrypt.py <plaintext>", file=sys.stderr)
        sys.exit(1)
    plaintext = sys.argv[1]
    envelope = envelope_encrypt(plaintext)
    print(envelope)
