import base64
from security_models import EncryptionRequest, EncryptionResponse
from security_client import (
    create_aws_kms_client,
    normalize_payload,
    encode_ciphertext_blob,
    normalize_encryption_context,
    build_metadata,
    handle_kms_error,
    validate_key_id,
    validate_plaintext,
)


def encrypt_payload(request: EncryptionRequest) -> EncryptionResponse:
    validate_key_id(request.key_id)
    validate_plaintext(request.plaintext)

    plaintext_bytes = normalize_payload(request.plaintext)
    encryption_context = normalize_encryption_context(request.encryption_context)

    kms_client = create_aws_kms_client()

    encrypt_kwargs = {
        "KeyId": request.key_id,
        "Plaintext": plaintext_bytes,
        "EncryptionAlgorithm": request.algorithm,
    }

    if encryption_context:
        encrypt_kwargs["EncryptionContext"] = encryption_context

    try:
        response = kms_client.encrypt(**encrypt_kwargs)
    except Exception as exc:
        raise handle_kms_error(exc, "encrypt")

    ciphertext_blob = response["CiphertextBlob"]
    encoded_ciphertext = encode_ciphertext_blob(ciphertext_blob)

    metadata = build_metadata(response)

    return EncryptionResponse(
        ciphertext_blob=encoded_ciphertext,
        key_id=response["KeyId"],
        encryption_algorithm=response["EncryptionAlgorithm"],
        request_id=metadata.get("request_id", ""),
        metadata=metadata,
    )
