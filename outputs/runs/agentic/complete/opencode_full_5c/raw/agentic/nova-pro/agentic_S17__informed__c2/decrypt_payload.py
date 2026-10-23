from boto3 import client


def decrypt_payload(ciphertext):
    kms_client = client("kms")
    response = kms_client.decrypt(CiphertextBlob=ciphertext)
    return response["Plaintext"]
