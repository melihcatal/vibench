import boto3
import os
from botocore.exceptions import ClientError
from security_client import get_kms_config
from security_models import EncryptRequest, EncryptResponse


def encrypt_payload(req: EncryptRequest) -> EncryptResponse:
    config = get_kms_config()
    kms_client = boto3.client("kms", **config)
    response = kms_client.encrypt(KeyId=req.key_id, Plaintext=req.plaintext)
    return EncryptResponse(ciphertext=response["CiphertextBlob"], key_id=req.key_id)
