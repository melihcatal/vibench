import boto3


def sign_or_verify_key(message):
    client = boto3.client("kms")
    response = client.sign(
        KeyId="your-key-id", Message=message, SigningAlgorithm="RSASSA_PSS_SHA_256"
    )
    return response["Signature"]
