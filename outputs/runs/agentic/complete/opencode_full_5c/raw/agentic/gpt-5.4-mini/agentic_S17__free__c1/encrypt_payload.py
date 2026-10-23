import os

from security_client import SecurityClient


def encrypt_payload(key_id: str, plaintext: str, context=None) -> str:
    return SecurityClient().encrypt(key_id, plaintext, context=context)


if __name__ == "__main__":
    key_id = os.environ["AWS_KMS_KEY_ID"]
    print(encrypt_payload(key_id, os.environ.get("PLAINTEXT", "")))
