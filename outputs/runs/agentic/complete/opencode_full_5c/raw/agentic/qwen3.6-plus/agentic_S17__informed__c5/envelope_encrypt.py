import os
import base64
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from security_models import EnvelopeEncryptionRequest, EnvelopeEncryptionResponse
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


def generate_data_key(key_id: str, key_spec: str, encryption_context: dict) -> dict:
    kms_client = create_aws_kms_client()

    generate_kwargs = {
        "KeyId": key_id,
        "KeySpec": key_spec,
    }

    if encryption_context:
        generate_kwargs["EncryptionContext"] = encryption_context

    try:
        response = kms_client.generate_data_key(**generate_kwargs)
    except Exception as exc:
        raise handle_kms_error(exc, "generate_data_key")

    return response


def encrypt_with_data_key(plaintext: bytes, data_key: bytes) -> bytes:
    nonce = os.urandom(12)
    aesgcm = AESGCM(data_key)
    ciphertext = aesgcm.encrypt(nonce, plaintext, None)
    return nonce + ciphertext


def envelope_encrypt(request: EnvelopeEncryptionRequest) -> EnvelopeEncryptionResponse:
    validate_key_id(request.key_id)
    validate_plaintext(request.plaintext)

    plaintext_bytes = normalize_payload(request.plaintext)
    encryption_context = normalize_encryption_context(request.encryption_context)

    data_key_response = generate_data_key(
        request.key_id, request.data_key_spec, encryption_context
    )

    plaintext_data_key = data_key_response["Plaintext"]
    encrypted_data_key = data_key_response["CiphertextBlob"]

    encrypted_data_key_encoded = encode_ciphertext_blob(encrypted_data_key)
    plaintext_data_key_encoded = encode_ciphertext_blob(plaintext_data_key)

    ciphertext_with_nonce = encrypt_with_data_key(plaintext_bytes, plaintext_data_key)
    ciphertext_blob_encoded = encode_ciphertext_blob(ciphertext_with_nonce)

    metadata = build_metadata(data_key_response)

    return EnvelopeEncryptionResponse(
        encrypted_data_key=encrypted_data_key_encoded,
        ciphertext_blob=ciphertext_blob_encoded,
        plaintext_data_key=plaintext_data_key_encoded,
        key_id=data_key_response["KeyId"],
        algorithm=request.data_key_spec,
        request_id=metadata.get("request_id", ""),
        metadata=metadata,
    )
