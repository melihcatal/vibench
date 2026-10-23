from security_client import get_security_client
from security_models import DecryptionRequest, DecryptionResponse


def decrypt_payload(request: DecryptionRequest) -> DecryptionResponse:
    kms_client = get_security_client()

    try:
        response = kms_client.decrypt(
            CiphertextBlob=request.ciphertext, KeyId=request.key_id
        )

        return DecryptionResponse(
            key_id=request.key_id, plaintext=response["Plaintext"]
        )
    except Exception as e:
        # In a real application, handle exceptions appropriately
        # For example, log the error and raise a custom exception
        print(f"An error occurred during decryption: {e}")
        raise
