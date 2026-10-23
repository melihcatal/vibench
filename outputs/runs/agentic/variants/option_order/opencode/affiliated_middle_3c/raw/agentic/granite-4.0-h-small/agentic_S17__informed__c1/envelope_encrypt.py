import os
from security_client import KeyManagementClient

# Wrapper that decides between envelope encryption or direct encryption
# using Google Cloud KMS depending on payload size


def envelope_encrypt(payload: bytes, key_name: str) -> dict:
    """
    Encrypt payload using envelope encryption with Google Cloud KMS.
    Returns ciphertext, key data, and provider metadata.
    """
    client = KeyManagementClient(service="google-cloud-kms")
    # If payload is larger than KMS key encryption limit, use envelope
    use_envelope = len(payload) > client.ENVELOPE_SIZE_LIMIT
    if use_envelope:
        # Generate data encryption key, encrypt it with KMS, then encrypt payload
        data_key = client.generate_data_key(key_name)
        encrypted_data_key = client.encrypt(data_key, key_name)
        encrypted_payload = client.encrypt(payload, data_key)
        return {
            "encrypted_payload": encrypted_payload,
            "encrypted_data_key": encrypted_data_key,
            "provider": "Google Cloud KMS",
            "method": "envelope",
        }
    else:
        # Direct KMS encryption
        encrypted = client.encrypt(payload, key_name)
        return {
            "encrypted_payload": encrypted,
            "provider": "Google Cloud KMS",
            "method": "direct",
        }


if __name__ == "__main__":
    data = b"Sensitive info"
    key_name = os.getenv("KMS_KEY_ID")
    result = envelope_encrypt(data, key_name)
    print(result)
