import base64
from cryptography.fernet import Fernet
from security_client import get_kms_client, AWS_KMS_KEY_ID


def envelope_encrypt_payload(plaintext: str) -> dict:
    kms_client = get_kms_client()
    if not AWS_KMS_KEY_ID:
        raise ValueError("AWS_KMS_KEY_ID environment variable not set.")

    data_key = kms_client.generate_data_key(KeyId=AWS_KMS_KEY_ID, KeySpec="AES_256")

    plaintext_key = data_key["Plaintext"]
    encrypted_data_key = data_key["CiphertextBlob"]

    f = Fernet(base64.urlsafe_b64encode(plaintext_key))
    encrypted_data = f.encrypt(plaintext.encode("utf-8"))

    return {
        "encrypted_data": encrypted_data.decode("utf-8"),
        "encrypted_data_key": base64.b64encode(encrypted_data_key).decode("utf-8"),
    }
