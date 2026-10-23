from security_models import (
    SigningRequest,
    SigningResponse,
    VerificationRequest,
    VerificationResponse,
)
from security_client import (
    create_aws_kms_client,
    normalize_payload,
    encode_ciphertext_blob,
    build_metadata,
    handle_kms_error,
    validate_key_id,
)


def sign_message(request: SigningRequest) -> SigningResponse:
    validate_key_id(request.key_id)

    message_bytes = normalize_payload(request.message)

    kms_client = create_aws_kms_client()

    sign_kwargs = {
        "KeyId": request.key_id,
        "Message": message_bytes,
        "SigningAlgorithm": request.signing_algorithm,
        "MessageType": request.message_type,
    }

    try:
        response = kms_client.sign(**sign_kwargs)
    except Exception as exc:
        raise handle_kms_error(exc, "sign")

    signature_encoded = encode_ciphertext_blob(response["Signature"])

    metadata = build_metadata(response)

    return SigningResponse(
        signature=signature_encoded,
        key_id=response["KeyId"],
        signing_algorithm=response["SigningAlgorithm"],
        request_id=metadata.get("request_id", ""),
        metadata=metadata,
    )


def verify_signature(request: VerificationRequest) -> VerificationResponse:
    validate_key_id(request.key_id)

    message_bytes = normalize_payload(request.message)
    signature_bytes = (
        bytes.fromhex(request.signature)
        if all(c in "0123456789abcdefABCDEF" for c in request.signature)
        else _decode_signature_blob(request.signature)
    )

    kms_client = create_aws_kms_client()

    verify_kwargs = {
        "KeyId": request.key_id,
        "Message": message_bytes,
        "Signature": signature_bytes,
        "SigningAlgorithm": request.signing_algorithm,
        "MessageType": request.message_type,
    }

    try:
        response = kms_client.verify(**verify_kwargs)
    except Exception as exc:
        raise handle_kms_error(exc, "verify")

    metadata = build_metadata(response)
    signature_valid = response.get("SignatureValid", False)

    return VerificationResponse(
        valid=signature_valid,
        key_id=response["KeyId"],
        signing_algorithm=response["SigningAlgorithm"],
        request_id=metadata.get("request_id", ""),
        metadata=metadata,
    )


def _decode_signature_blob(signature: str) -> bytes:
    import base64

    try:
        return base64.b64decode(signature)
    except Exception:
        return signature.encode("utf-8")
