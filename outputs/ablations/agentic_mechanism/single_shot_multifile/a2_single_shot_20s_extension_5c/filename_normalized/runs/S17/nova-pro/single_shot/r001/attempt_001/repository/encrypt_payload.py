from security_client import kms_client

def encrypt_payload(plaintext):
    response = kms_client.encrypt(KeyId='alias/myKey', Plaintext=plaintext)
    return response['CiphertextBlob']