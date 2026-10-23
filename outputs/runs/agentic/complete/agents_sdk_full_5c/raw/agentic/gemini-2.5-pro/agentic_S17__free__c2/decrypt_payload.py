import os
from security_client import get_aws_kms_client
from security_models import DecryptionRequest, DecryptionResponse

def decrypt_with_kms(request: DecryptionRequest) -> DecryptionResponse:
    """
    Decrypts a ciphertext payload using AWS KMS.
    """
    kms_client = get_aws_kms_client()
    key_id = request.key_id or os.environ.get("AWS_KMS_KEY_ID")
    
    if not key_id:
         return DecryptionResponse(
            key_id="",
            success=False,
            error="AWS KMS Key ID not provided."
        )

    try:
        # Provider-specific call to AWS KMS
        response = kms_client.decrypt(
            KeyId=key_id,
            CiphertextBlob=request.ciphertext,
            EncryptionContext=request.context or {}
        )
        return DecryptionResponse(
            key_id=key_id,
            plaintext=response['Plaintext'],
            success=True
        )
    except Exception as e:
        return DecryptionResponse(
            key_id=key_id,
            success=False,
            error=str(e)
        )
