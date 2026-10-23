from boto3 import client


def encrypt_payload(plaintext):
    kms_client = client("kms")
    response = kms_client.encrypt(KeyId="alias/example_key", Plaintext=plaintext)
    return response["CiphertextBlob"]
