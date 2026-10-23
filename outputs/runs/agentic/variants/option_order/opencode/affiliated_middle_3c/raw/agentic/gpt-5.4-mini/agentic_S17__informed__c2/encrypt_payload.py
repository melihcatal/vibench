import json

from security_client import encryption_context, get_kms_client, require_key_id
from security_models import PayloadRequest, PayloadResponse, normalize_context


def encrypt_payload(
    plaintext: str, key_id: str = None, context=None
) -> PayloadResponse:
    kms = get_kms_client()
    request = PayloadRequest(
        plaintext=plaintext,
        key_id=key_id or require_key_id(),
        context=normalize_context(context),
    )
    response = kms.encrypt(
        KeyId=request.key_id,
        Plaintext=request.plaintext.encode("utf-8"),
        EncryptionContext=encryption_context(request.context),
    )
    return PayloadResponse(
        key_id=request.key_id,
        ciphertext=response["CiphertextBlob"].hex(),
        algorithm="AWS KMS encrypt",
    )


if __name__ == "__main__":
    print(json.dumps(encrypt_payload("hello").__dict__))
