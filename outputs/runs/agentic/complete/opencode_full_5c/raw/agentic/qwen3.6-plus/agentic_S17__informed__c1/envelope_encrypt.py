import os
import base64
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from security_client import (
    AWSSecurityClient,
    normalize_plaintext,
    encode_bytes_to_base64,
)
from security_models import EnvelopeEncryptionRequest, load_kms_config


def envelope_encrypt(
    plaintext: str, key_id: str, encryption_context: dict = None
) -> dict:
    config = load_kms_config()
    client = AWSSecurityClient(config)

    plaintext_bytes = normalize_plaintext(plaintext)
    request = EnvelopeEncryptionRequest(
        key_id=key_id,
        plaintext=plaintext_bytes,
        encryption_context=encryption_context,
        number_of_bytes=32,
    )

    data_key_response = client.generate_data_key(request)
    plaintext_data_key = data_key_response["plaintext_data_key"]
    encrypted_data_key = data_key_response["encrypted_data_key"]

    aesgcm = AESGCM(plaintext_data_key)
    nonce = os.urandom(12)
    ciphertext = aesgcm.encrypt(nonce, plaintext_bytes, None)

    combined_ciphertext = nonce + ciphertext

    return {
        "encrypted_data_key": encode_bytes_to_base64(encrypted_data_key),
        "ciphertext_blob": encode_bytes_to_base64(combined_ciphertext),
        "key_id": data_key_response["key_id"],
        "encryption_algorithm": "AES_256_GCM",
        "request_id": data_key_response["request_id"],
    }


if __name__ == "__main__":
    key_id = os.environ.get("AWS_KMS_KEY_ID", "")
    plaintext = os.environ.get("PAYLOAD_PLAINTEXT", "envelope-encrypted-data")
    result = envelope_encrypt(plaintext, key_id)
    print(result)
