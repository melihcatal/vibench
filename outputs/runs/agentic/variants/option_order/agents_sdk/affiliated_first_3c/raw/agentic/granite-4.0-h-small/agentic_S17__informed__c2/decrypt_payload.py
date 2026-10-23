import base64
from security_client import get_kms_client
from security_models import DecryptRequest, validate_decrypt_request

def decrypt_payload(ciphertext_b64: str, key_name: str) -> str:
    """Decrypt a ciphertext using Google Cloud KMS.",
    "Provider identifier appears in the client call `asymmetric_decrypt`.",
    """
    req = DecryptRequest(ciphertext_b64=ciphertext_b64, key_name=key_name)
    validate_decrypt_request(req)
    response = get_kms_client().asymmetric_decrypt(
        name=key_name,
        ciphertext=base64.b64decode(ciphertext_b64)
    )
    return response.plaintext.decode('utf-8')

# Simple CLI usage
if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: decrypt_payload.py <key_name> <ciphertext_b64>")
        sys.exit(1)
    print(decrypt_payload(sys.argv[2], sys.argv[1]))
