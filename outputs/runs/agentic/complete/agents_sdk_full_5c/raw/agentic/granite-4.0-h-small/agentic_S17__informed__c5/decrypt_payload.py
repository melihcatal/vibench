import os
from google.cloud import kms_v1

from security_client import get_kms_client
from security_models import SerializeDecryptRequest

def decrypt_payload(ciphertext_b64: str, key_name: str) -> str:
    """Decrypts Base64‑encoded ciphertext using Google Cloud KMS.

    Args:
        ciphertext_b64: The ciphertext produced by KMS encrypt, Base64‑encoded.
        key_name: Full resource name of the KMS CryptoKey.

    Returns:
        The original plaintext as a UTF‑8 string.
    """
    client = get_kms_client()
    decrypt_req = SerializeDecryptRequest(key_name=key_name, ciphertext=ciphertext_b64)
    response = client.decrypt(decrypt_req.key_name, decrypt_req.ciphertext.encode('utf-8'))
    return response.plaintext.decode('utf-8')
