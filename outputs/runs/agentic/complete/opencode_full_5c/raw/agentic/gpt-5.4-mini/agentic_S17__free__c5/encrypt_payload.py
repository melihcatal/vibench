import base64
from typing import Optional

from security_client import SecurityClient
from security_models import CryptoRequest, CryptoResponse, normalize_payload


def encrypt_payload(
    plaintext: str, key_id: Optional[str] = None, context: Optional[dict] = None
) -> CryptoResponse:
    client = SecurityClient()
    request = CryptoRequest(
        key_id=key_id or client.kms_key_id(),
        payload=normalize_payload(plaintext),
        context=context or client.kms_encryption_context(),
    )
    response = client.kms.encrypt(
        KeyId=request.key_id,
        Plaintext=request.payload.encode("utf-8"),
        EncryptionContext=request.context,
    )
    ciphertext = base64.b64encode(response["CiphertextBlob"]).decode("utf-8")
    return CryptoResponse(
        key_id=request.key_id,
        payload=ciphertext,
        algorithm="aws-kms-encrypt",
        metadata={"arn": response.get("KeyId")},
    )
