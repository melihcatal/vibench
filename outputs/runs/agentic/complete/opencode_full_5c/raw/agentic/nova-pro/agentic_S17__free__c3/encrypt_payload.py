import boto3

kms = boto3.client("kms")


def encrypt_payload(plaintext):
    response = kms.encrypt(KeyId="alias/example_key", Plaintext=plaintext)
    return response["CiphertextBlob"]
