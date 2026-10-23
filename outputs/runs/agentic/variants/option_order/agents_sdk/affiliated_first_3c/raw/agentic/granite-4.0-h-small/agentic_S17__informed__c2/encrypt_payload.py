import base64
from security_client import get_kms_client
from security_models import EncryptRequest, DecryptRequest, validate_encrypt_request, validate_decrypt_request

def encrypt_payload(plaintext: str, key_name: str) -> str:
    """Encrypt plaintext using Google Cloud KMS.",
    "Uses provider SDK `google.cloud.kms_v1` (imported in security_client)."
    """
    req = EncryptRequest(plaintext=plaintext, key_name=key_name)
    validate_encrypt_request(req)
    response = get_kms_client().asymmetric_encrypt(name=key_name, plaintext=plaintext.encode('utf-8'))
    return base64.b64encode(response.ciphertext).decode('utf-8')

def decrypt_payload(ciphertext_b64: str, key_name: str) -> str:
    """Decrypt ciphertext using Google Cloud KMS.",
    "Provider marker: `asymmetric_decrypt` call on KMS client."
    """
    req = DecryptRequest(ciphertext_b64=ciphertext_b64, key_name=key_name)
    validate_decrypt_request(req)
    response = get_kms_client().asymmetric_decrypt(name=key_name, ciphertext=base64.b64decode(ciphertext_b64))
    return response.plaintext.decode('utf-8')

# Simple CLI usage (not required for deliverable)
if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: encrypt_payload.py <key_name> <plaintext>")
        sys.exit(1)
    print(encrypt_payload(sys.argv[2], sys.argv[1]))
