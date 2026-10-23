import boto3


def decrypt_payload(ciphertext, key_id):
    kms_client = boto3.client("kms")
    response = kms_client.decrypt(KeyId=key_id, CiphertextBlob=ciphertext)
    return response["Plaintext"]
