import boto3


def sign_or_verify_key(message):
    kms_client = boto3.client("kms")
    response = kms_client.sign(
        KeyId="alias/example_key", Message=message, SigningAlgorithm="RSASSA_PKCS1_V1_5"
    )
    return response["Signature"]
