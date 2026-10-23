from security_client import get_kms_client

def decrypt_payload(ciphertext):
    client = get_kms_client()
    response = client.decrypt(CiphertextBlob=ciphertext)
    return response['Plaintext']