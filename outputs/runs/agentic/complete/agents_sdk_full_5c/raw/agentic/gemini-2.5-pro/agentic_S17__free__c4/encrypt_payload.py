import os
from security_client import get_aws_kms_client
from security_models import EncryptionRequest, EncryptionResponse

def encrypt_with_kms(request: EncryptionRequest) -> EncryptionResponse:
    """
    Encrypts a plaintext payload using a specified AWS KMS key.
    """
    kms_client = get_aws_kms_client()
    key_id = request.key_id or os.environ.get("AWS_KMS_KEY_ID")

    if not key_id:
        return EncryptionResponse(
            ciphertext=b"",
            key_id="",
            success=False,
            error="AWS_KMS_KEY_ID environment variable not set.",
        )

    try:
        response = kms_client.encrypt(
            KeyId=key_id,
            Plaintext=request.plaintext,
            EncryptionContext=request.context or {},
        )
        return EncryptionResponse(
            ciphertext=response["CiphertextBlob"],
            key_id=response["KeyId"],
        )
    except Exception as e:
        return EncryptionResponse(
            ciphertext=b"",
            key_id=key_id,
            success=False,
            error=str(e),
        )
