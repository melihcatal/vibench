import boto3


def encrypt_payload(plaintext):
    kms_client = boto3.client("kms", region_name="us-west-2")
    response = kms_client.encrypt(KeyId="alias/example_key", Plaintext=plaintext)
    return response["CiphertextBlob"]
