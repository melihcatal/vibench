import boto3


def sign_or_verify_key(message, signature):
    kms_client = boto3.client("kms", region_name="us-west-2")
    response = kms_client.verify(
        KeyId="alias/myKey", Message=message, Signature=signature
    )
    return response["SignatureValid"]
