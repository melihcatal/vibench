import os
import sys
import json
import base64
from .security_client import get_security_config
from .security_models import SecurityModels

if __name__ == "__main__":
    # Expect JSON body via stdin: {"plaintext": "", "key_name": ""}
    raw = sys.stdin.read()
    data = json.loads(raw)
    plaintext = data.get("plaintext")
    key_name = data.get("key_name")
    if not plaintext:
        print("Missing plaintext", file=sys.stderr)
        sys.exit(1)
    if not key_name:
        print("Missing key_name", file=sys.stderr)
        sys.exit(1)
    config = get_security_config()
    client = config.client()
    algorithm = "RSA-OAEP-256"  # Example; adapt per provider
    if config.service == "aws":
        # AWS KMS generate-data-key without encryption context returns plaintext data key
        resp = client.generate_data_key(KeyId=key_name, KeySpec="AES_256")  # type: ignore
        plaintext_key = resp["Plaintext"]
        # Encrypt plaintext using generated symmetric key (local AES) – for demo only
        aes_key_b64 = base64.b64encode(plaintext_key).decode()
        ciphertext = SecurityModels.encrypt_aes(plaintext, aes_key_b64)
        output = {"key": aes_key_b64, "ciphertext": ciphertext}
    elif config.service == "azure":
        # Azure Key Vault Key generate key and then encrypt
        # First generate a symmetric key in Key Vault
        generated_key = client.create_key(key_name, "oct-256")  # type: ignore
        # Retrieve the generated key's value (Vault stores it encrypted; for demo we assume we can
        # fetch the plaintext value via the SDK – in production you would handle this securely)
        fetched_key = client.get_key(key_name).attributes.id
        # Encrypt using the Vault generated key via Vault's transit endpoint (simulate here)
        transit_path = f"transit/encrypt/{key_name.split('/')[-1]}"
        resp = client.sys.call_secret(
            transit_path,
            json={"plaintext": base64.b64encode(plaintext.encode()).decode()},
        )
        ciphertext = resp["data"]["ciphertext"]
        output = {"ciphertext": ciphertext}
    elif config.service == "hashicorp":
        # Vault transit envelope encryption
        transit_path = f"transit/encrypt/{key_name.split('/')[-1]}"
        resp = client.sys.call_secret(
            transit_path,
            json={"plaintext": base64.b64encode(plaintext.encode()).decode()},
        )
        output = {"ciphertext": resp["data"]["ciphertext"]}
    else:
        raise RuntimeError("Unsupported service")
    print(json.dumps(output, indent=2))


# Simple local AES encryption helper (not using external provider; purely local)
def encrypt_aes(plaintext: str, key_b64: str) -> str:
    from Crypto.Cipher import AES
    import hashlib

    # Derive AES key from base64 input (assume 256-bit)
    key = base64.b64decode(key_b64)
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(plaintext.encode())
    return base64.b64encode(ciphertext).decode()
