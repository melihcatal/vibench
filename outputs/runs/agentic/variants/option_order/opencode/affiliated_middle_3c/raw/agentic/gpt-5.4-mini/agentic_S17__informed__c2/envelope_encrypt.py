import json

from security_client import (
    b64encode_bytes,
    encryption_context,
    get_kms_client,
    require_key_id,
)
from security_models import normalize_context


def envelope_encrypt(plaintext: str, key_id: str = None, context=None):
    kms = get_kms_client()
    key_id = key_id or require_key_id()
    data_key = kms.generate_data_key(
        KeyId=key_id,
        KeySpec="AES_256",
        EncryptionContext=encryption_context(normalize_context(context)),
    )
    return {
        "key_id": key_id,
        "encrypted_data_key": b64encode_bytes(data_key["CiphertextBlob"]),
        "plaintext": plaintext,
        "algorithm": "AWS KMS envelope encryption",
    }


if __name__ == "__main__":
    print(json.dumps(envelope_encrypt("hello")))
