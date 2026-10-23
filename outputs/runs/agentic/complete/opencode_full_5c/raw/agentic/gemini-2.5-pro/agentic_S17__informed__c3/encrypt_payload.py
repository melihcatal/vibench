from security_client import get_kms_client
from security_models import EncryptRequest, EncryptResponse


def encrypt_payload(request: EncryptRequest) -> EncryptResponse:
    """
    Encrypts a plaintext payload with a managed key using AWS KMS.
    """
    kms_client = get_kms_client()

    try:
        response = kms_client.encrypt(
            KeyId=request.key_id,
            Plaintext=request.plaintext,
            EncryptionContext=request.encryption_context or {},
        )
        return EncryptResponse(
            ciphertext=response["CiphertextBlob"], key_id=response["KeyId"]
        )
    except Exception as e:
        # In a real application, you'd want more robust error handling
        print(f"An error occurred during encryption: {e}")
        return EncryptResponse(ciphertext=b"", key_id=request.key_id, success=False)
