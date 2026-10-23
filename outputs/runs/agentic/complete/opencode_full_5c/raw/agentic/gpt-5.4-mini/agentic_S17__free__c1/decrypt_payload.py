import os

from security_client import SecurityClient


def decrypt_payload(key_id: str, ciphertext_b64: str, context=None) -> str:
    return SecurityClient().decrypt(key_id, ciphertext_b64, context=context)


if __name__ == "__main__":
    key_id = os.environ["AWS_KMS_KEY_ID"]
    print(decrypt_payload(key_id, os.environ.get("CIPHERTEXT_B64", "")))
