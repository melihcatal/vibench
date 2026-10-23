import boto3


def sign_or_verify_key(message, key_id):
    client = boto3.client("kms")
    response = client.sign(
        KeyId=key_id, Message=message, SigningAlgorithm="RSASSA_PKCS1_V1_5_SHA_256"
    )
    return response["Signature"]
