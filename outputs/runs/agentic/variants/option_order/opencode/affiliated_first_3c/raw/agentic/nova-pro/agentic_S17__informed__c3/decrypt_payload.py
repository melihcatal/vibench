import boto3
from botocore.exceptions import ClientError


def decrypt_payload(ciphertext):
    client = boto3.client("kms")
    try:
        response = client.decrypt(CiphertextBlob=ciphertext)
        return response["Plaintext"]
    except ClientError as e:
        print(e)
        return None
