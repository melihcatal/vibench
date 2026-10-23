import boto3


def encrypt_payload(plaintext, key_id):
    client = boto3.client("kms", region_name="us-west-2")
    response = client.encrypt(KeyId=key_id, Plaintext=plaintext)
    return response["CiphertextBlob"]
