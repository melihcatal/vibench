from typing import Optional, Dict, List

from security_client import get_kms_client, resolve_key_id, parse_kms_error
from security_models import (
    SignRequest,
    SignResponse,
    VerifyRequest,
    VerifyResponse,
    SigningAlgorithm,
    MessageType,
    normalize_plaintext,
    validate_key_id,
    encode_signature,
    decode_signature,
)


def sign_message(
    message: str,
    key_id: str,
    signing_algorithm: SigningAlgorithm = SigningAlgorithm.RSASSA_PKCS1_V1_5_SHA_256,
    message_type: MessageType = MessageType.RAW,
    grant_tokens: Optional[List[str]] = None,
) -> SignResponse:
    kms_client = get_kms_client()
    resolved_key_id = resolve_key_id(validate_key_id(key_id))
    message_bytes = normalize_plaintext(message)

    sign_params = {
        "KeyId": resolved_key_id,
        "Message": message_bytes,
        "SigningAlgorithm": signing_algorithm.value,
        "MessageType": message_type.value,
    }

    if grant_tokens:
        sign_params["GrantTokens"] = grant_tokens

    request = SignRequest(
        key_id=resolved_key_id,
        message=message_bytes,
        signing_algorithm=signing_algorithm,
        message_type=message_type,
        grant_tokens=grant_tokens,
    )

    try:
        response = kms_client.sign(**sign_params)
        return SignResponse(
            signature=response["Signature"],
            key_id=response["KeyId"],
            signing_algorithm=response["SigningAlgorithm"],
            request_id=response["ResponseMetadata"]["RequestId"],
            http_status_code=response["ResponseMetadata"]["HTTPStatusCode"],
        )
    except Exception as e:
        error_info = parse_kms_error(e)
        raise RuntimeError(
            f"AWS KMS Sign failed for key {resolved_key_id}: "
            f"[{error_info['error_code']}] {error_info['error_message']}"
        ) from e


def verify_signature(
    message: str,
    signature: bytes,
    key_id: str,
    signing_algorithm: SigningAlgorithm = SigningAlgorithm.RSASSA_PKCS1_V1_5_SHA_256,
    message_type: MessageType = MessageType.RAW,
    grant_tokens: Optional[List[str]] = None,
) -> VerifyResponse:
    kms_client = get_kms_client()
    resolved_key_id = resolve_key_id(validate_key_id(key_id))
    message_bytes = normalize_plaintext(message)

    verify_params = {
        "KeyId": resolved_key_id,
        "Message": message_bytes,
        "Signature": signature,
        "SigningAlgorithm": signing_algorithm.value,
        "MessageType": message_type.value,
    }

    if grant_tokens:
        verify_params["GrantTokens"] = grant_tokens

    request = VerifyRequest(
        key_id=resolved_key_id,
        message=message_bytes,
        signature=signature,
        signing_algorithm=signing_algorithm,
        message_type=message_type,
        grant_tokens=grant_tokens,
    )

    try:
        response = kms_client.verify(**verify_params)
        return VerifyResponse(
            signature_valid=response["SignatureValid"],
            key_id=response["KeyId"],
            signing_algorithm=response["SigningAlgorithm"],
            request_id=response["ResponseMetadata"]["RequestId"],
            http_status_code=response["ResponseMetadata"]["HTTPStatusCode"],
        )
    except Exception as e:
        error_info = parse_kms_error(e)
        raise RuntimeError(
            f"AWS KMS Verify failed for key {resolved_key_id}: "
            f"[{error_info['error_code']}] {error_info['error_message']}"
        ) from e


def sign_and_encode(
    message: str,
    key_id: str,
    signing_algorithm: SigningAlgorithm = SigningAlgorithm.RSASSA_PKCS1_V1_5_SHA_256,
) -> Dict[str, str]:
    response = sign_message(
        message=message,
        key_id=key_id,
        signing_algorithm=signing_algorithm,
    )
    return {
        "signature": encode_signature(response.signature),
        "key_id": response.key_id,
        "signing_algorithm": response.signing_algorithm,
        "request_id": response.request_id,
    }


def verify_with_encoded_signature(
    message: str,
    signature_b64: str,
    key_id: str,
    signing_algorithm: SigningAlgorithm = SigningAlgorithm.RSASSA_PKCS1_V1_5_SHA_256,
) -> Dict[str, object]:
    signature_bytes = decode_signature(signature_b64)
    response = verify_signature(
        message=message,
        signature=signature_bytes,
        key_id=key_id,
        signing_algorithm=signing_algorithm,
    )
    return {
        "signature_valid": response.signature_valid,
        "key_id": response.key_id,
        "signing_algorithm": response.signing_algorithm,
        "request_id": response.request_id,
    }
