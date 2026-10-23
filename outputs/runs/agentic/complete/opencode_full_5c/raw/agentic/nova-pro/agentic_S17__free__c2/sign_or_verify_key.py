import boto3

kms = boto3.client("kms", region_name="us-west-2")


def sign_or_verify_key(message, signature):
    response = kms.verify(
        KeyId="alias/myKey",
        Message=message,
        Signature=signature,
        SigningAlgorithm="RSASSA_PSS_SHA_256",
    )
    return response["SignatureValid"]
