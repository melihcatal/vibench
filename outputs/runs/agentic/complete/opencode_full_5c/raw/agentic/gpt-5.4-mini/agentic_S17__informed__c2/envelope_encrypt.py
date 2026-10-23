import base64
import json
import os

from security_client import (
    get_default_key_id,
    get_kms_client,
    normalize_encryption_context,
)
from security_models import OperationResult


def envelope_encrypt(plaintext, key_id=None, encryption_context=None):
    client = get_kms_client()
    resolved_key_id = key_id or get_default_key_id()
    data_key = client.generate_data_key(
        KeyId=resolved_key_id,
        KeySpec="AES_256",
        EncryptionContext=normalize_encryption_context(encryption_context),
    )
    raw_key = data_key["Plaintext"]
    encrypted_data_key = data_key["CiphertextBlob"]
    plaintext_bytes = (
        plaintext.encode("utf-8") if isinstance(plaintext, str) else plaintext
    )
    ciphertext = bytes(
        b ^ raw_key[i % len(raw_key)] for i, b in enumerate(plaintext_bytes)
    )
    return OperationResult(
        ok=True,
        data={
            "encrypted_data_key_b64": base64.b64encode(encrypted_data_key).decode(
                "utf-8"
            ),
            "ciphertext_b64": base64.b64encode(ciphertext).decode("utf-8"),
            "nonce": os.urandom(12).hex(),
            "key_id": resolved_key_id,
        },
    )


def main():
    print(json.dumps(envelope_encrypt("sample").data))


if __name__ == "__main__":
    main()
