import os
import base64
import boto3
from botocore.exceptions import ClientError
from security_models import DecryptionRequest, DecryptionResponse
from security_client import get_kms_client, validate_key_id


def decrypt_payload(ciphertext, key_id=None, encryption_context=None):
    request = DecryptionRequest(
        ciphertext=ciphertext,
        key_id=key_id or os.environ.get("AWS_KMS_KEY_ID"),
        encryption_context=encryption_context,
    )
    validate_key_id(request.key_id)
    client = get_kms_client()
    try:
        ciphertext_bytes = base64.b64decode(request.ciphertext)
        kwargs = {
            "CiphertextBlob": ciphertext_bytes,
        }
        if request.encryption_context:
            kwargs["EncryptionContext"] = request.encryption_context
        response = client.decrypt(**kwargs)
        plaintext = response["Plaintext"].decode("utf-8")
        return DecryptionResponse(
            plaintext=plaintext,
            key_id=response["KeyId"],
            encryption_algorithm=response.get(
                "EncryptionAlgorithm", "SYMMETRIC_DEFAULT"
            ),
            request_id=response.get("ResponseMetadata", {}).get("RequestId", ""),
        )
    except ClientError as e:
        raise RuntimeError(
            f"AWS KMS decrypt failed: {e.response['Error']['Message']}"
        ) from e
