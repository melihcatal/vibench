import os
import base64
import boto3
from botocore.config import Config
from security_models import DecryptRequest, DecryptResponse
from security_client import get_kms_client, load_aws_config


def decrypt_payload(
    ciphertext_b64: str, key_id: str = None, encryption_context: dict = None
) -> DecryptResponse:
    config = load_aws_config()
    kms_client = get_kms_client(config)

    ciphertext_blob = base64.b64decode(ciphertext_b64)

    request = DecryptRequest(
        key_id=key_id or os.environ.get("AWS_KMS_KEY_ID"),
        ciphertext_blob=ciphertext_blob,
        encryption_context=encryption_context or {},
    )

    params = {
        "CiphertextBlob": request.ciphertext_blob,
    }
    if request.key_id:
        params["KeyId"] = request.key_id
    if request.encryption_context:
        params["EncryptionContext"] = request.encryption_context

    response = kms_client.decrypt(**params)

    plaintext = response["Plaintext"].decode("utf-8")

    return DecryptResponse(
        plaintext=plaintext,
        key_id=response.get("KeyId", ""),
        encryption_algorithm=response.get("EncryptionAlgorithm", "SYMMETRIC_DEFAULT"),
        request_id=response.get("ResponseMetadata", {}).get("RequestId", ""),
    )


if __name__ == "__main__":
    result = decrypt_payload("base64encodedciphertext==")
    print(result.plaintext)
