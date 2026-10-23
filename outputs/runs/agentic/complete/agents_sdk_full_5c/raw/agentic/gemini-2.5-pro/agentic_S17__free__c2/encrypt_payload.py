import os
from security_client import get_aws_kms_client
from security_models import EncryptionRequest, EncryptionResponse

def encrypt_with_kms(request: EncryptionRequest) -> EncryptionResponse:
    """
    Encrypts a plaintext payload using AWS KMS.
    """
    kms_client = get_aws_kms_client()
    key_id = request.key_id or os.environ.get("AWS_KMS_KEY_ID")

    if not key_id:
        return EncryptionResponse(
            key_id="",
            ciphertext=b"",
            success=False,
            error="AWS KMS Key ID not provided."
        )

    try:
        # Provider-specific call to AWS KMS
        response = kms_client.encrypt(
            KeyId=key_id,
            Plaintext=request.plaintext,
            EncryptionContext=request.context or {}
        )
        return EncryptionResponse(
            key_id=key_id,
            ciphertext=response['CiphertextBlob'],
            success=True
        )
    except Exception as e:
        return EncryptionResponse(
            key_id=key_id,
            ciphertext=b"",
            success=False,
            error=str(e)
        )
