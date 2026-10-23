from __future__ import annotations

import hashlib
from typing import Dict, Any

from security_client import DEFAULT_KMS_SIGNING_ALGORITHM, kms_client
from security_models import SignVerifyRequest, SignVerifyResponse, b64decode_text, b64encode_bytes, text_to_bytes



def _kms_message_and_type(message: str, signing_algorithm: str):
    if signing_algorithm.endswith("SHA_256"):
        return hashlib.sha256(text_to_bytes(message)).digest(), "DIGEST"
    if signing_algorithm.endswith("SHA_384"):
        return hashlib.sha384(text_to_bytes(message)).digest(), "DIGEST"
    if signing_algorithm.endswith("SHA_512"):
        return hashlib.sha512(text_to_bytes(message)).digest(), "DIGEST"
    return text_to_bytes(message), "RAW"



def sign_or_verify_key(request: SignVerifyRequest) -> SignVerifyResponse:
    client = kms_client()
    algorithm = request.signing_algorithm or DEFAULT_KMS_SIGNING_ALGORITHM
    message, message_type = _kms_message_and_type(request.message, algorithm)
    if request.verify:
        response = client.verify(
            KeyId=request.key_id,
            Message=message,
            MessageType=message_type,
            Signature=b64decode_text(request.signature_b64 or ""),
            SigningAlgorithm=algorithm,
        )
        return SignVerifyResponse(
            key_id=request.key_id,
            operation="verify",
            verified=response["SignatureValid"],
            algorithm=response.get("SigningAlgorithm", algorithm),
        )
    response = client.sign(
        KeyId=request.key_id,
        Message=message,
        MessageType=message_type,
        SigningAlgorithm=algorithm,
    )
    return SignVerifyResponse(
        key_id=request.key_id,
        operation="sign",
        signature_b64=b64encode_bytes(response["Signature"]),
        algorithm=response.get("SigningAlgorithm", algorithm),
    )



def sign_message_dict(key_id: str, message: str, signing_algorithm: str = DEFAULT_KMS_SIGNING_ALGORITHM) -> Dict[str, Any]:
    result = sign_or_verify_key(SignVerifyRequest(key_id=key_id, message=message, signing_algorithm=signing_algorithm, verify=False))
    return {
        "provider": result.provider,
        "key_id": result.key_id,
        "operation": result.operation,
        "signature_b64": result.signature_b64,
        "algorithm": result.algorithm,
    }



def verify_message_dict(key_id: str, message: str, signature_b64: str, signing_algorithm: str = DEFAULT_KMS_SIGNING_ALGORITHM) -> Dict[str, Any]:
    result = sign_or_verify_key(SignVerifyRequest(key_id=key_id, message=message, signature_b64=signature_b64, signing_algorithm=signing_algorithm, verify=True))
    return {
        "provider": result.provider,
        "key_id": result.key_id,
        "operation": result.operation,
        "verified": result.verified,
        "algorithm": result.algorithm,
    }
