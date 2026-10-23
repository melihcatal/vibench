import os
import base64
import boto3
from botocore.config import Config
from security_models import EncryptRequest, EncryptResponse
from security_client import get_kms_client, load_aws_config


def encrypt_payload(
    plaintext: str, key_id: str = None, encryption_context: dict = None
) -> EncryptResponse:
    config = load_aws_config()
    kms_client = get_kms_client(config)

    request = EncryptRequest(
        key_id=key_id or os.environ.get("AWS_KMS_KEY_ID"),
        plaintext=plaintext,
        encryption_context=encryption_context or {},
    )

    plaintext_bytes = request.plaintext.encode("utf-8")

    params = {
        "KeyId": request.key_id,
        "Plaintext": plaintext_bytes,
    }
    if request.encryption_context:
        params["EncryptionContext"] = request.encryption_context

    response = kms_client.encrypt(**params)

    ciphertext_blob = response["CiphertextBlob"]
    ciphertext_b64 = base64.b64encode(ciphertext_blob).decode("utf-8")

    return EncryptResponse(
        ciphertext=ciphertext_b64,
        key_id=response["KeyId"],
        encryption_algorithm=response.get("EncryptionAlgorithm", "SYMMETRIC_DEFAULT"),
        request_id=response.get("ResponseMetadata", {}).get("RequestId", ""),
    )


if __name__ == "__main__":
    result = encrypt_payload("Sensitive data to encrypt")
    print(result.ciphertext[:50])
