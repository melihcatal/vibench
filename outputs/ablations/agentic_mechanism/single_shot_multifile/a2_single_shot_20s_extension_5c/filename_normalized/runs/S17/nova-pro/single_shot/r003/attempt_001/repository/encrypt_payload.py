from security_client import get_kms_client

def encrypt_payload(plaintext):
    client = get_kms_client()
    response = client.encrypt(KeyId='alias/myKey', Plaintext=plaintext)
    return response['CiphertextBlob']