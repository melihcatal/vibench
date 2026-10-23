import os
import base64
from security_client import AWSSecurityClient, normalize_ciphertext
from security_models import DecryptionRequest, load_kms_config


def decrypt_payload(
    ciphertext_blob_b64: str, key_id: str = None, encryption_context: dict = None
) -> dict:
    config = load_kms_config()
    client = AWSSecurityClient(config)

    ciphertext_bytes = normalize_ciphertext(ciphertext_blob_b64)
    request = DecryptionRequest(
        ciphertext_blob=ciphertext_bytes,
        encryption_context=encryption_context,
    )

    response = client.decrypt(request)
    return {
        "plaintext": response.plaintext.decode("utf-8"),
        "key_id": response.key_id,
        "encryption_algorithm": response.encryption_algorithm,
        "request_id": response.request_id,
    }


if __name__ == "__main__":
    ciphertext = os.environ.get("PAYLOAD_CIPHERTEXT", "")
    result = decrypt_payload(ciphertext)
    print(result)
