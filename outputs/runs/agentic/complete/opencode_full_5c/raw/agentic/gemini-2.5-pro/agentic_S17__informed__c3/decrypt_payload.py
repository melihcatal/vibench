from security_client import get_kms_client
from security_models import DecryptRequest, DecryptResponse


def decrypt_payload(request: DecryptRequest) -> DecryptResponse:
    """
    Decrypts a ciphertext payload with a managed key using AWS KMS.
    """
    kms_client = get_kms_client()

    try:
        response = kms_client.decrypt(
            KeyId=request.key_id,
            CiphertextBlob=request.ciphertext,
            EncryptionContext=request.encryption_context or {},
        )
        return DecryptResponse(
            plaintext=response["Plaintext"], key_id=response["KeyId"]
        )
    except Exception as e:
        print(f"An error occurred during decryption: {e}")
        return DecryptResponse(plaintext=b"", key_id=request.key_id, success=False)
