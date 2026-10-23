from security_client import get_kms_client
from security_models import encode_base64, decode_base64
from cryptography.fernet import Fernet


def envelope_encrypt(key_id: str, plaintext: str) -> tuple[str, str]:
    kms_client = get_kms_client()
    response = kms_client.generate_data_key(KeyId=key_id, KeySpec="AES_256")
    data_key_plaintext = response["Plaintext"]
    encrypted_data_key_blob = response["CiphertextBlob"]

    fernet = Fernet(base64.urlsafe_b64encode(data_key_plaintext))
    encrypted_payload = fernet.encrypt(plaintext.encode("utf-8"))

    return encode_base64(encrypted_data_key_blob), encode_base64(encrypted_payload)


def envelope_decrypt(encrypted_data_key_b64: str, encrypted_payload_b64: str) -> str:
    kms_client = get_kms_client()
    encrypted_data_key_blob = decode_base64(encrypted_data_key_b64)

    response = kms_client.decrypt(CiphertextBlob=encrypted_data_key_blob)
    data_key_plaintext = response["Plaintext"]

    encrypted_payload = decode_base64(encrypted_payload_b64)
    fernet = Fernet(base64.urlsafe_b64encode(data_key_plaintext))
    decrypted_payload = fernet.decrypt(encrypted_payload)

    return decrypted_payload.decode("utf-8")
