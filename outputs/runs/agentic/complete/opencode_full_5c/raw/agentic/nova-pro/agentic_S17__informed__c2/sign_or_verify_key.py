from boto3 import client


def sign_or_verify_key(data):
    kms_client = client("kms")
    response = kms_client.sign(
        KeyId="alias/example_key", Message=data, SigningAlgorithm="RSASSA_PSS_SHA_256"
    )
    return response["Signature"]


def verify_signature(data, signature):
    kms_client = client("kms")
    response = kms_client.verify(
        KeyId="alias/example_key",
        Message=data,
        Signature=signature,
        SigningAlgorithm="RSASSA_PSS_SHA_256",
    )
    return response["SignatureValid"]
