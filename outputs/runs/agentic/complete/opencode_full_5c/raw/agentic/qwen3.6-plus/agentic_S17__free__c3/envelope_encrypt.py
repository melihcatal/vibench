import base64
import os
from typing import Any, Dict, Optional

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding as sym_padding

from security_client import AWS_KMS_KEY_ID, create_kms_client, load_config_from_env
from security_models import (
    EnvelopeEncryptionRequest,
    EnvelopeEncryptionResponse,
    normalize_payload,
    serialize_response,
)


def envelope_encrypt(
    plaintext: str,
    key_id: Optional[str] = None,
    encryption_context: Optional[Dict[str, str]] = None,
    data_key_spec: str = "AES_256",
) -> EnvelopeEncryptionResponse:
    config = load_config_from_env()
    client = create_kms_client(region=config.get("aws_default_region"))

    resolved_key_id = key_id or os.environ.get("AWS_KMS_KEY_ID", "")
    if not resolved_key_id:
        raise ValueError(
            "AWS_KMS_KEY_ID environment variable or key_id parameter is required"
        )

    normalized = normalize_payload(plaintext)

    data_key_response = client.generate_data_key(
        key_id=resolved_key_id,
        key_spec=data_key_spec,
        encryption_context=encryption_context,
    )

    plaintext_data_key = data_key_response["Plaintext"]
    encrypted_data_key = data_key_response["CiphertextBlob"]
    kms_key_id = data_key_response["KeyId"]
    request_id = data_key_response.get("ResponseMetadata", {}).get("RequestId", "")

    iv = os.urandom(16)
    padder = sym_padding.PKCS7(128).padder()
    padded_data = padder.update(normalized.encode("utf-8")) + padder.finalize()

    cipher = Cipher(algorithms.AES(plaintext_data_key), modes.GCM(iv))
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    tag = encryptor.tag

    encrypted_payload = base64.b64encode(iv + tag + ciphertext).decode("utf-8")
    encrypted_data_key_b64 = base64.b64encode(encrypted_data_key).decode("utf-8")

    response = EnvelopeEncryptionResponse(
        encrypted_data_key=encrypted_data_key_b64,
        ciphertext_blob=encrypted_payload,
        key_id=kms_key_id,
        request_id=request_id,
    )
    return response


def envelope_decrypt(
    encrypted_data_key: str,
    ciphertext_blob: str,
    encryption_context: Optional[Dict[str, str]] = None,
) -> str:
    config = load_config_from_env()
    client = create_kms_client(region=config.get("aws_default_region"))

    encrypted_data_key_bytes = base64.b64decode(encrypted_data_key)

    decrypt_params = {"CiphertextBlob": encrypted_data_key_bytes}
    if encryption_context:
        decrypt_params["EncryptionContext"] = encryption_context

    data_key_response = client.client.decrypt(**decrypt_params)
    plaintext_data_key = data_key_response["Plaintext"]

    encrypted_data = base64.b64decode(ciphertext_blob)
    iv = encrypted_data[:16]
    tag = encrypted_data[16:32]
    ciphertext = encrypted_data[32:]

    cipher = Cipher(algorithms.AES(plaintext_data_key), modes.GCM(iv, tag))
    decryptor = cipher.decryptor()
    padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()

    unpadder = sym_padding.PKCS7(128).unpadder()
    plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()

    return plaintext.decode("utf-8")


def envelope_encrypt_and_serialize(
    plaintext: str,
    key_id: Optional[str] = None,
    encryption_context: Optional[Dict[str, str]] = None,
) -> str:
    response = envelope_encrypt(
        plaintext=plaintext,
        key_id=key_id,
        encryption_context=encryption_context,
    )
    return serialize_response(response)


def envelope_encrypt_with_metadata(
    plaintext: str,
    key_id: str,
    metadata: Dict[str, str],
) -> Dict[str, Any]:
    response = envelope_encrypt(
        plaintext=plaintext,
        key_id=key_id,
        encryption_context=metadata,
    )
    return {
        "encrypted_data_key": response.encrypted_data_key,
        "ciphertext_blob": response.ciphertext_blob,
        "key_id": response.key_id,
        "request_id": response.request_id,
        "metadata": metadata,
        "timestamp": response.timestamp,
    }
