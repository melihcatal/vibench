import boto3
from botocore.exceptions import ClientError
from security_client import get_kms_config
from security_models import SignRequest, SignResponse, VerifyRequest


def sign_message(req: SignRequest) -> SignResponse:
    config = get_kms_config()
    kms_client = boto3.client("kms", **config)
    response = kms_client.sign(
        KeyId=req.key_id,
        Message=req.message,
        SigningAlgorithm="RSASSA_PKCS1_V1_5_SHA_256",
        MessageType="RAW",
    )
    return SignResponse(signature=response["Signature"])


def verify_signature(req: VerifyRequest) -> bool:
    config = get_kms_config()
    kms_client = boto3.client("kms", **config)
    try:
        kms_client.verify(
            KeyId=req.key_id,
            Message=req.message,
            Signature=req.signature,
            SigningAlgorithm="RSASSA_PKCS1_V1_5_SHA_256",
            MessageType="RAW",
        )
        return True
    except ClientError:
        return False
