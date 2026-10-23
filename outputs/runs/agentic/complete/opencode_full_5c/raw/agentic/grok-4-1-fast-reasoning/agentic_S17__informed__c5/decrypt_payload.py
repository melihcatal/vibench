from security_client import get_kms_client, get_key_arn


def decrypt_payload(ciphertext: bytes) -> bytes:
    client = get_kms_client()
    key_arn = get_key_arn()
    response = client.decrypt(KeyId=key_arn, CiphertextBlob=ciphertext)
    return response["Plaintext"]
