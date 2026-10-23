import os
import base64
from security_client import (
    AWSSecurityClient,
    normalize_plaintext,
    encode_bytes_to_base64,
)
from security_models import EncryptionRequest, EncryptionAlgorithm, load_kms_config


def encrypt_payload(
    plaintext: str, key_id: str, encryption_context: dict = None
) -> dict:
    config = load_kms_config()
    client = AWSSecurityClient(config)

    plaintext_bytes = normalize_plaintext(plaintext)
    request = EncryptionRequest(
        key_id=key_id,
        plaintext=plaintext_bytes,
        encryption_context=encryption_context,
        algorithm=EncryptionAlgorithm.SYMMETRIC_DEFAULT,
    )

    response = client.encrypt(request)
    return {
        "ciphertext_blob": encode_bytes_to_base64(response.ciphertext_blob),
        "key_id": response.key_id,
        "encryption_algorithm": response.encryption_algorithm,
        "request_id": response.request_id,
    }


if __name__ == "__main__":
    key_id = os.environ.get("AWS_KMS_KEY_ID", "")
    plaintext = os.environ.get("PAYLOAD_PLAINTEXT", "sensitive-data-to-encrypt")
    result = encrypt_payload(plaintext, key_id)
    print(result)
