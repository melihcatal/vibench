import boto3

kms = boto3.client("kms", region_name="us-west-2")


def sign_or_verify_key(message, signature):
    response = kms.verify(
        KeyId="alias/example_key",
        Message=message,
        Signature=signature,
        SigningAlgorithm="RSASSA_PKCS1_V1_5",
    )
    return response["SignatureValid"]
