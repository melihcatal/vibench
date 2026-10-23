from __future__ import annotations

from security_client import ensure_dict, kms_client, normalize_kms_key_id
from security_models import EncryptRequest, EncryptResponse, b64encode_text


def encrypt_payload(request: EncryptRequest) -> EncryptResponse:
    client = kms_client()
    response = client.encrypt(
        KeyId=normalize_kms_key_id(request.key_id),
        Plaintext=request.plaintext.encode("utf-8"),
        EncryptionContext=ensure_dict(request.encryption_context),
    )
    return EncryptResponse(
        key_id=response["KeyId"],
        ciphertext_b64=b64encode_text(response["CiphertextBlob"]),
    )
