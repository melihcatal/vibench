import boto3
from botocore.exceptions import ClientError


def encrypt_payload(plaintext):
    client = boto3.client("kms")
    try:
        response = client.encrypt(KeyId="alias/example_key", Plaintext=plaintext)
        return response["CiphertextBlob"]
    except ClientError as e:
        print(e)
        return None
