from security_client import kms_client

def decrypt_payload(ciphertext):
    response = kms_client.decrypt(CiphertextBlob=ciphertext)
    return response['Plaintext']