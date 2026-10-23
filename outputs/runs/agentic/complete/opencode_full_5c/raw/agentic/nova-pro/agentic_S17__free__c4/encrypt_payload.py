import boto3

kms = boto3.client("kms", region_name="us-west-2")


def encrypt_payload(plaintext):
    response = kms.encrypt(KeyId="alias/example_key", Plaintext=plaintext)
    return response["CiphertextBlob"]
