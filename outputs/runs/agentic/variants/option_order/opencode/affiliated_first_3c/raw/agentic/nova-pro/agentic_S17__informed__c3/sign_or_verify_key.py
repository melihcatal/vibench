import boto3
from botocore.exceptions import ClientError


def sign_or_verify_key(message):
    client = boto3.client("kms")
    try:
        response = client.sign(
            KeyId="alias/example_key", Message=message, MessageType="RAW"
        )
        return response["Signature"]
    except ClientError as e:
        print(e)
        return None
