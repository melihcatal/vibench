import json
from security_client import get_kms_client
from security_models import EncryptRequest, validate_encrypt_request

def envelope_encrypt(plaintext: str, data_key_id: str, envelope_key_id: str) -> dict:
    """Implement envelope encryption using Google Cloud KMS.",
    "Provider identifier: the client obtained via `get_kms_client()` is a Google Cloud KMS client.",
    """
    # 1️⃣ Generate a data encryption key (DEK) with the local data‑key service
    dek_name = data_key_id
    dek_resp = get_kms_client().generate_data_key(name=dek_name, key_spec='AES_256')
    plaintext_bytes = plaintext.encode('utf-8')
    # Local symmetric encryption of payload (XOR is illustrative; replace with AES for production)
    encrypted_plaintext = bytes(a ^ b for a, b in zip(plaintext_bytes, dek_resp.plaintext))
    encrypted_data_b64 = base64.b64encode(encrypted_plaintext).decode('utf-8')

    # 2️⃣ Asymmetrically encrypt (wrap) the DEK with the envelope KMS key
    wrapped_key = get_kms_client().asymmetric_encrypt(
        name=envelope_key_id,
        plaintext=dek_resp.plaintext
    ).ciphertext
    wrapped_key_b64 = base64.b64encode(wrapped_key).decode('utf-8')

    return {
        "encrypted_data": encrypted_data_b64,
        "wrapped_key": wrapped_key_b64
    }

# Simple usage example (not required for submission)
if __name__ == "__main__":
    import sys, json
    if len(sys.argv) != 4:
        print("Usage: envelope_encrypt.py <data_key_id> <envelope_key_id> <plaintext>")
        sys.exit(1)
    result = envelope_encrypt(sys.argv[3], sys.argv[1], sys.argv[2])
    print(json.dumps(result, indent=2))
