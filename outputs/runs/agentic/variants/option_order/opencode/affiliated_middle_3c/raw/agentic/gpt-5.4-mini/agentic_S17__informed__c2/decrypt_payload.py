import json

from security_client import (
    b64decode_text,
    encryption_context,
    get_kms_client,
    require_key_id,
)
from security_models import PayloadResponse, normalize_context


def decrypt_payload(
    ciphertext: str, key_id: str = None, context=None
) -> PayloadResponse:
    kms = get_kms_client()
    response = kms.decrypt(
        CiphertextBlob=b64decode_text(ciphertext),
        EncryptionContext=encryption_context(normalize_context(context)),
    )
    return PayloadResponse(
        key_id=key_id or require_key_id(),
        ciphertext=ciphertext,
        plaintext=response["Plaintext"].decode("utf-8"),
        algorithm="AWS KMS decrypt",
    )


if __name__ == "__main__":
    print(json.dumps(decrypt_payload("").__dict__))
