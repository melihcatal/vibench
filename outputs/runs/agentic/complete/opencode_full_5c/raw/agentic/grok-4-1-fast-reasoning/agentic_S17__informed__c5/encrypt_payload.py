from security_client import get_kms_client, get_key_arn


def encrypt_payload(plaintext: bytes) -> bytes:
    client = get_kms_client()
    key_arn = get_key_arn()
    response = client.encrypt(KeyId=key_arn, Plaintext=plaintext)
    return response["CiphertextBlob"]
