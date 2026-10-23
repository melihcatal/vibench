import base64
from cryptography.fernet import Fernet
from security_client import get_security_client


def envelope_encrypt(key_id: str, plaintext: bytes) -> dict:
    kms_client = get_security_client()

    data_key_response = kms_client.generate_data_key(KeyId=key_id, KeySpec="AES_256")

    plaintext_data_key = data_key_response["Plaintext"]
    encrypted_data_key_blob = data_key_response["CiphertextBlob"]

    f = Fernet(base64.urlsafe_b64encode(plaintext_data_key))
    encrypted_payload = f.encrypt(plaintext)

    return {
        "encrypted_data_key": base64.b64encode(encrypted_data_key_blob).decode("utf-8"),
        "encrypted_payload": base64.b64encode(encrypted_payload).decode("utf-8"),
    }


def envelope_decrypt(
    key_id: str, encrypted_data_key: str, encrypted_payload: str
) -> bytes:
    kms_client = get_security_client()

    decoded_encrypted_data_key = base64.b64decode(encrypted_data_key)

    decrypted_key_response = kms_client.decrypt(
        CiphertextBlob=decoded_encrypted_data_key, KeyId=key_id
    )

    plaintext_data_key = decrypted_key_response["Plaintext"]

    f = Fernet(base64.urlsafe_b64encode(plaintext_data_key))
    decrypted_payload = f.decrypt(base64.b64decode(encrypted_payload))

    return decrypted_payload
