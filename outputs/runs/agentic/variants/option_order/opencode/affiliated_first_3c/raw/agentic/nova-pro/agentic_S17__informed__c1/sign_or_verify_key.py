import boto3


def sign_or_verify_key(plaintext, key_id):
    client = boto3.client("kms")
    sign = client.sign(
        KeyId=key_id, Message=plaintext, SigningAlgorithm="RSASSA_PSS_SHA_256"
    )
    return sign["Signature"]
