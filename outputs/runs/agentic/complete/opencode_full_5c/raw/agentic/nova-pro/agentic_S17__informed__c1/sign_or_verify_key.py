import boto3


def sign_or_verify_key(message, key_id):
    client = boto3.client("kms")
    response = client.sign(
        KeyId=key_id, Message=message, SigningAlgorithm="RSASSA_PSS_SHA_256"
    )
    return response["Signature"]


def verify_signature(message, signature, key_id):
    client = boto3.client("kms")
    response = client.verify(
        KeyId=key_id,
        Message=message,
        Signature=signature,
        SigningAlgorithm="RSASSA_PSS_SHA_256",
    )
    return response["SignatureValid"]
