from __future__ import annotations

from security_client import AwsKmsSecurityClient, encode_blob, decode_blob
from security_models import SignRequest, VerifyRequest, normalize_bytes_payload

AWS_KMS_SERVICE = "AWS Key Management Service"


def sign_or_verify_key(message, key_id: str, signature_b64: str | None = None) -> dict:
    client = AwsKmsSecurityClient()
    message_bytes = normalize_bytes_payload(message)
    if signature_b64:
        response = client.verify(
            VerifyRequest(
                message=message_bytes,
                signature=decode_blob(signature_b64),
                key_id=key_id,
            )
        )
        return {
            "service": AWS_KMS_SERVICE,
            "key_id": response.key_id,
            "verified": response.verified,
            "algorithm": response.algorithm,
            "metadata": response.metadata,
        }
    response = client.sign(SignRequest(message=message_bytes, key_id=key_id))
    return {
        "service": AWS_KMS_SERVICE,
        "key_id": response.key_id,
        "signature_b64": encode_blob(response.signature),
        "algorithm": response.algorithm,
        "metadata": response.metadata,
    }
