import os
from security_client import KmsClient
from security_models import DecryptRequest, DecryptResponse

# Use AWS KMS as the concrete provider (identifiable by the service name)
client = KmsClient(service="AWS Key Management Service", region="us-east-1")


def check_payload_safety(plaintext: str) -> bool:
    """Simple unsafe‑content check on decrypted payloads.

    Returns True if the text is considered safe (does not contain dangerous patterns).
    """
    # Example unsafe patterns – in production use a more robust detector or ML model
    unsafe_patterns = [
        "rm -rf /",
        "DROP TABLE",
        "EXEC master.",
        "user=\\w+\\s+password=\\w+",
    ]
    for pat in unsafe_patterns:
        if pat in plaintext:
            return False
    return True


def safely_decrypt(request: DecryptRequest) -> DecryptResponse:
    """Decrypt a payload and validate it for unsafe content before returning it."""
    # Perform the actual decryption via the concrete provider
    response = client.decrypt(
        CiphertextBlob=request["ciphertext_blob"], KeyId=request["key_id"]
    )
    plaintext = response["Plaintext"].decode()
    if not check_payload_safety(plaintext):
        raise ValueError("Decrypted payload contains unsafe content")
    return {"Plaintext": plaintext}
