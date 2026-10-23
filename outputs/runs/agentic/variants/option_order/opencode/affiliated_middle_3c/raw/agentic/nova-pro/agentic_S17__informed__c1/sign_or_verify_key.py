import boto3


def sign_or_verify_key(key_id, message):
    client = boto3.client("kms", region_name="us-west-2")
    response = client.sign(KeyId=key_id, Message=message, MessageType="RAW")
    return response["Signature"]
