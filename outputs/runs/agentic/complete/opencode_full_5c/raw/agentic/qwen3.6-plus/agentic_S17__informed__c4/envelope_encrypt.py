import os
import base64
import boto3
from botocore.exceptions import ClientError
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from security_models import EnvelopeEncryptionRequest, EnvelopeEncryptionResponse
from security_client import get_kms_client, validate_key_id, generate_data_key


def envelope_encrypt(plaintext, key_id=None, encryption_context=None):
    request = EnvelopeEncryptionRequest(
        plaintext=plaintext,
        key_id=key_id or os.environ.get("AWS_KMS_KEY_ID"),
        encryption_context=encryption_context,
    )
    validate_key_id(request.key_id)
    client = get_kms_client()
    try:
        data_key_response = generate_data_key(
            client, request.key_id, request.encryption_context
        )
        plaintext_key = base64.b64decode(data_key_response["plaintext_key"])
        encrypted_key = base64.b64decode(data_key_response["encrypted_key"])
        aesgcm = AESGCM(plaintext_key)
        nonce = AESGCM.generate_nonce(bit_length=96)
        plaintext_bytes = (
            request.plaintext.encode("utf-8")
            if isinstance(request.plaintext, str)
            else request.plaintext
        )
        ciphertext = aesgcm.encrypt(nonce, plaintext_bytes, None)
        return EnvelopeEncryptionResponse(
            encrypted_data_key=base64.b64encode(encrypted_key).decode("utf-8"),
            nonce=base64.b64encode(nonce).decode("utf-8"),
            ciphertext=base64.b64encode(ciphertext).decode("utf-8"),
            key_id=data_key_response["key_id"],
            encryption_algorithm="AES_256_GCM",
        )
    except ClientError as e:
        raise RuntimeError(
            f"AWS KMS envelope encryption failed: {e.response['Error']['Message']}"
        ) from e
