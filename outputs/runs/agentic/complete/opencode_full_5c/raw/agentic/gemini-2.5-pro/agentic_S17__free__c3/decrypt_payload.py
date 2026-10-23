import base64
from security_client import get_kms_client


def decrypt_payload(ciphertext_b64: str) -> str:
    kms_client = get_kms_client()

    try:
        ciphertext_blob = base64.b64decode(ciphertext_b64)
        response = kms_client.decrypt(CiphertextBlob=ciphertext_blob)
        return response["Plaintext"].decode("utf-8")
    except Exception as e:
        print(f"Decryption failed: {e}")
        return ""
