import os
from typing import Optional, Dict, Any

from security_client import SecurityClient, KMSClientConfig, DEFAULT_SIGNING_KEY_ID
from security_models import (
    SignRequest,
    VerifyRequest,
    SignResponse,
    VerifyResponse,
    SigningAlgorithm,
    MessageType,
    normalize_payload_to_bytes,
    encode_ciphertext_blob,
    decode_ciphertext_blob,
    response_to_dict,
)

AWS_KMS_REGION = os.environ.get(
    "AWS_DEFAULT_REGION", os.environ.get("AWS_REGION", "us-east-1")
)
DEFAULT_SIGNING_ALGORITHM = os.environ.get(
    "DEFAULT_SIGNING_ALGORITHM", "RSASSA_PSS_SHA_256"
)


def _resolve_signing_algorithm(algorithm_str: str) -> SigningAlgorithm:
    mapping = {
        "RSASSA_PSS_SHA_256": SigningAlgorithm.RSASSA_PSS_SHA_256,
        "RSASSA_PSS_SHA_384": SigningAlgorithm.RSASSA_PSS_SHA_384,
        "RSASSA_PSS_SHA_512": SigningAlgorithm.RSASSA_PSS_SHA_512,
        "RSASSA_PKCS1_V1_5_SHA_256": SigningAlgorithm.RSASSA_PKCS1_V1_5_SHA_256,
        "ECDSA_SHA_256": SigningAlgorithm.ECDSA_SHA_256,
        "ECDSA_SHA_384": SigningAlgorithm.ECDSA_SHA_384,
    }
    return mapping.get(algorithm_str, SigningAlgorithm.RSASSA_PSS_SHA_256)


def sign_message(
    message: Any,
    key_id: Optional[str] = None,
    signing_algorithm: Optional[str] = None,
    message_type: MessageType = MessageType.RAW,
    client: Optional[SecurityClient] = None,
) -> Dict[str, Any]:
    target_key_id = key_id or DEFAULT_SIGNING_KEY_ID
    if not target_key_id:
        raise ValueError(
            "No KMS signing key ID provided. Set DEFAULT_KMS_SIGNING_KEY_ID or pass key_id explicitly."
        )

    algo = _resolve_signing_algorithm(signing_algorithm or DEFAULT_SIGNING_ALGORITHM)

    request = SignRequest(
        key_id=target_key_id,
        message=message,
        signing_algorithm=algo,
        message_type=message_type,
    )

    kms_client = client or SecurityClient()
    response = kms_client.sign(request)

    result = response_to_dict(response)
    result["message_length"] = len(normalize_payload_to_bytes(message))
    return result


def verify_signature(
    message: Any,
    signature: Any,
    key_id: Optional[str] = None,
    signing_algorithm: Optional[str] = None,
    message_type: MessageType = MessageType.RAW,
    client: Optional[SecurityClient] = None,
) -> Dict[str, Any]:
    target_key_id = key_id or DEFAULT_SIGNING_KEY_ID
    if not target_key_id:
        raise ValueError(
            "No KMS signing key ID provided. Set DEFAULT_KMS_SIGNING_KEY_ID or pass key_id explicitly."
        )

    algo = _resolve_signing_algorithm(signing_algorithm or DEFAULT_SIGNING_ALGORITHM)

    if isinstance(signature, str):
        signature_bytes = decode_ciphertext_blob(signature)
    elif isinstance(signature, bytes):
        signature_bytes = signature
    else:
        signature_bytes = bytes(signature)

    request = VerifyRequest(
        key_id=target_key_id,
        message=message,
        signature=signature_bytes,
        signing_algorithm=algo,
        message_type=message_type,
    )

    kms_client = client or SecurityClient()
    response = kms_client.verify(request)

    result = response_to_dict(response)
    result["message_length"] = len(normalize_payload_to_bytes(message))
    return result


def sign_and_verify(
    message: Any,
    key_id: Optional[str] = None,
    signing_algorithm: Optional[str] = None,
    client: Optional[SecurityClient] = None,
) -> Dict[str, Any]:
    sign_result = sign_message(
        message=message,
        key_id=key_id,
        signing_algorithm=signing_algorithm,
        client=client,
    )

    verify_result = verify_signature(
        message=message,
        signature=sign_result["signature"],
        key_id=key_id,
        signing_algorithm=signing_algorithm,
        client=client,
    )

    return {
        "sign": sign_result,
        "verify": verify_result,
        "signature_valid": verify_result["signature_valid"],
    }
