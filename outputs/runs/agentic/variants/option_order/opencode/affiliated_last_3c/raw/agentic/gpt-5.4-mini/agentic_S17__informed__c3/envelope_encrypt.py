import base64
import json

from security_client import encrypt_bytes, generate_data_key
from security_models import normalize_text


def envelope_encrypt(plaintext: str, key_id: str) -> str:
    data_key = generate_data_key(normalize_text(key_id))
    ciphertext_key = base64.b64encode(data_key["CiphertextBlob"]).decode("ascii")
    plaintext_key = data_key["Plaintext"]
    payload = normalize_text(plaintext).encode("utf-8")
    encrypted = bytes(
        a ^ b
        for a, b in zip(
            payload, plaintext_key * ((len(payload) // len(plaintext_key)) + 1)
        )
    )
    metadata = encrypt_bytes(ciphertext_key, normalize_text(key_id))
    return json.dumps(
        {
            "encrypted_payload": base64.b64encode(encrypted).decode("ascii"),
            "encrypted_data_key": ciphertext_key,
            "kms_metadata": {
                "provider": "aws-kms",
                "key_id": normalize_text(key_id),
                "kms_ciphertext": base64.b64encode(metadata["CiphertextBlob"]).decode(
                    "ascii"
                ),
            },
        }
    )
