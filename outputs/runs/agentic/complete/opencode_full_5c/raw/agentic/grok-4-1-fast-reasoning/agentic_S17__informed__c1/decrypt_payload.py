import boto3
import os
from botocore.exceptions import ClientError
from security_client import get_kms_config
from security_models import DecryptRequest, DecryptResponse


def decrypt_payload(req: DecryptRequest) -> DecryptResponse:
    config = get_kms_config()
    kms_client = boto3.client("kms", **config)
    kwargs = {"CiphertextBlob": req.ciphertext}
    if req.key_id:
        kwargs["KeyId"] = req.key_id
    response = kms_client.decrypt(**kwargs)
    return DecryptResponse(plaintext=response["Plaintext"])
