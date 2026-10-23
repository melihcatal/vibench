import boto3

kms = boto3.client("kms")


def sign_or_verify_key(message, signature):
    response = kms.verify(
        KeyId="alias/example_key", Message=message, Signature=signature
    )
    return response["SignatureValid"]
