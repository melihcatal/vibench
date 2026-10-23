import base64
from typing import Optional

from security_client import SecurityClient
from security_models import CryptoRequest, CryptoResponse, normalize_payload


def decrypt_payload(
    ciphertext: str, key_id: Optional[str] = None, context: Optional[dict] = None
) -> CryptoResponse:
    client = SecurityClient()
    request = CryptoRequest(
        key_id=key_id or client.kms_key_id(),
        payload=normalize_payload(ciphertext),
        context=context or client.kms_encryption_context(),
    )
    blob = base64.b64decode(request.payload.encode("utf-8"))
    response = client.kms.decrypt(
        CiphertextBlob=blob, EncryptionContext=request.context
    )
    plaintext = response["Plaintext"].decode("utf-8")
    return CryptoResponse(
        key_id=request.key_id or response.get("KeyId", ""),
        payload=plaintext,
        algorithm="aws-kms-decrypt",
        metadata={"arn": response.get("KeyId")},
    )
