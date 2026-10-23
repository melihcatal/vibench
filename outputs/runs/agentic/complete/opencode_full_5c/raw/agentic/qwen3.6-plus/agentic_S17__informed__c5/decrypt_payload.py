from security_models import DecryptionRequest, DecryptionResponse
from security_client import (
    create_aws_kms_client,
    decode_ciphertext_blob,
    normalize_encryption_context,
    build_metadata,
    handle_kms_error,
    validate_ciphertext,
)


def decrypt_payload(request: DecryptionRequest) -> DecryptionResponse:
    validate_ciphertext(request.ciphertext_blob)

    ciphertext_bytes = decode_ciphertext_blob(request.ciphertext_blob)
    encryption_context = normalize_encryption_context(request.encryption_context)

    kms_client = create_aws_kms_client()

    decrypt_kwargs = {
        "CiphertextBlob": ciphertext_bytes,
        "EncryptionAlgorithm": request.algorithm,
    }

    if request.key_id:
        decrypt_kwargs["KeyId"] = request.key_id

    if encryption_context:
        decrypt_kwargs["EncryptionContext"] = encryption_context

    try:
        response = kms_client.decrypt(**decrypt_kwargs)
    except Exception as exc:
        raise handle_kms_error(exc, "decrypt")

    plaintext = response["Plaintext"].decode("utf-8", errors="replace")

    metadata = build_metadata(response)

    return DecryptionResponse(
        plaintext=plaintext,
        key_id=response["KeyId"],
        encryption_algorithm=response["EncryptionAlgorithm"],
        request_id=metadata.get("request_id", ""),
        metadata=metadata,
    )
