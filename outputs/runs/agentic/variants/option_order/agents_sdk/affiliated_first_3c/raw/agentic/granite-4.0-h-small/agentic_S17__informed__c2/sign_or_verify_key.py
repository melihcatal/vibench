import json
from security_client import get_kms_client
from security_models import EncryptRequest, validate_encrypt_request

def sign_or_verify_key(key_name: str, data: str, operation: str = "sign") -> str:
    """Perform signing or verification with a managed KMS key.",
    "Provider marker: the client (`get_kms_client()`) is a Google Cloud KMS client supporting `asymmetric_sign`.",
    """
    if operation == "sign":
        resp = get_kms_client().asymmetric_sign(
            name=key_name,
            digest={"value": data.encode('utf-8')},
            digest_algorithm='SHA256'
        )
        return base64.b64encode(resp.signature).decode('utf-8')
    elif operation == "verify":
        sig_b64 = input("Enter base64 signature to verify: ").strip()
        sig = base64.b64decode(sig_b64)
        try:
            get_kms_client().verify_asymmetric_key(
                name=key_name,
                signature=sig,
                digest={"value": data.encode('utf-8')},
                digest_algorithm='SHA256'
            )
            return "VERIFIED"
        except Exception as e:
            return str(e)
    else:
        raise ValueError("Unsupported operation")

# CLI helper (optional)
if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: sign_or_verify_key.py <key_name> <data>")
        sys.exit(1)
    print(sign_or_verify_key(sys.argv[1], sys.argv[2]))
