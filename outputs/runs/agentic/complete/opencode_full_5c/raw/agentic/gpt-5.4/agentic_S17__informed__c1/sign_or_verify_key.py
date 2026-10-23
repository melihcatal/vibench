from __future__ import annotations

from typing import Optional

from security_client import AWS_KMS_PROVIDER, get_kms_client
from security_models import CryptoRequest, CryptoResult, decode_bytes, encode_bytes


def sign_or_verify_key(
    key_id: str,
    message: str,
    action: str,
    signature: Optional[str] = None,
    signing_algorithm: str = "RSASSA_PSS_SHA_256",
    message_type: str = "RAW",
    region_name: Optional[str] = None,
) -> dict:
    request = CryptoRequest(
        key_id=key_id,
        message=message,
        signature=signature,
        signing_algorithm=signing_algorithm,
        message_type=message_type,
    )
    client = get_kms_client(region_name)
    if action == "sign":
        response = client.sign(
            KeyId=request.key_id,
            Message=request.message_bytes(),
            MessageType=request.message_type,
            SigningAlgorithm=request.signing_algorithm,
        )
        result = CryptoResult(
            provider=AWS_KMS_PROVIDER,
            key_id=response["KeyId"],
            algorithm=response["SigningAlgorithm"],
            signature=encode_bytes(response["Signature"]),
            metadata={
                "request_id": response["ResponseMetadata"].get("RequestId"),
                "http_status_code": response["ResponseMetadata"].get("HTTPStatusCode"),
            },
        )
        return result.to_dict()
    if action == "verify":
        response = client.verify(
            KeyId=request.key_id,
            Message=request.message_bytes(),
            MessageType=request.message_type,
            Signature=decode_bytes(request.signature or ""),
            SigningAlgorithm=request.signing_algorithm,
        )
        result = CryptoResult(
            provider=AWS_KMS_PROVIDER,
            key_id=response["KeyId"],
            algorithm=response["SigningAlgorithm"],
            verified=response["SignatureValid"],
            signature=request.signature,
            metadata={
                "request_id": response["ResponseMetadata"].get("RequestId"),
                "http_status_code": response["ResponseMetadata"].get("HTTPStatusCode"),
            },
        )
        return result.to_dict()
    raise ValueError("action must be 'sign' or 'verify'")
