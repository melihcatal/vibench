import os
import base64
import boto3
from botocore.exceptions import ClientError
from security_models import EncryptionRequest, EncryptionResponse, normalize_payload
from security_client import get_kms_client, validate_key_id


def encrypt_payload(plaintext, key_id=None, encryption_context=None):
    request = EncryptionRequest(
        plaintext=plaintext,
        key_id=key_id or os.environ.get("AWS_KMS_KEY_ID"),
        encryption_context=encryption_context,
    )
    validate_key_id(request.key_id)
    normalized = normalize_payload(request.plaintext)
    client = get_kms_client()
    try:
        kwargs = {
            "KeyId": request.key_id,
            "Plaintext": normalized.encode("utf-8")
            if isinstance(normalized, str)
            else normalized,
        }
        if request.encryption_context:
            kwargs["EncryptionContext"] = request.encryption_context
        response = client.encrypt(**kwargs)
        ciphertext_blob = response["CiphertextBlob"]
        return EncryptionResponse(
            ciphertext=base64.b64encode(ciphertext_blob).decode("utf-8"),
            key_id=response["KeyId"],
            encryption_algorithm=response.get(
                "EncryptionAlgorithm", "SYMMETRIC_DEFAULT"
            ),
            request_id=response.get("ResponseMetadata", {}).get("RequestId", ""),
        )
    except ClientError as e:
        raise RuntimeError(
            f"AWS KMS encrypt failed: {e.response['Error']['Message']}"
        ) from e
