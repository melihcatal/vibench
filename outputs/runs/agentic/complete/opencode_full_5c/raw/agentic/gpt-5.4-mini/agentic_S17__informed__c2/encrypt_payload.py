import json

from security_client import (
    get_default_key_id,
    get_kms_client,
    normalize_encryption_context,
    to_b64,
)
from security_models import OperationResult, PayloadEnvelope, normalize_text


def encrypt_payload(plaintext, key_id=None, encryption_context=None):
    client = get_kms_client()
    payload = normalize_text(plaintext).encode("utf-8")
    resolved_key_id = key_id or get_default_key_id()
    response = client.encrypt(
        KeyId=resolved_key_id,
        Plaintext=payload,
        EncryptionContext=normalize_encryption_context(encryption_context),
    )
    ciphertext = response["CiphertextBlob"]
    envelope = PayloadEnvelope(
        plaintext=normalize_text(plaintext),
        ciphertext=ciphertext,
        key_id=resolved_key_id,
        context=normalize_encryption_context(encryption_context),
    )
    return OperationResult(
        ok=True,
        data={
            "ciphertext_b64": to_b64(ciphertext),
            "key_id": resolved_key_id,
            "envelope": envelope.__dict__,
        },
    )


def main():
    print(json.dumps(encrypt_payload("sample").data))


if __name__ == "__main__":
    main()
