import os
from security_client import AWSKMSClient
from security_models import DecryptRequest, normalize_decrypt_response


def decrypt_payload(ciphertext_hex: str) -> dict:
    """
    Decrypts a ciphertext payload using AWS KMS.

    Args:
        ciphertext_hex: Hex-encoded ciphertext to decrypt.

    Returns:
        Dictionary containing plaintext and metadata.
    """
    client = AWSKMSClient()
    ciphertext = bytes.fromhex(ciphertext_hex)
    request = DecryptRequest(ciphertext=ciphertext)

    response = client.decrypt(ciphertext=request.ciphertext)

    normalized_response = normalize_decrypt_response(response)
    return {
        "plaintext": normalized_response.plaintext.decode("utf-8"),
        "key_id": normalized_response.key_id,
        "algorithm": normalized_response.algorithm,
    }
