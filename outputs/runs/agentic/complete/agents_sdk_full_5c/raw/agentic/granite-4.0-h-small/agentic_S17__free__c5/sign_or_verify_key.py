import os
import json
from security_client import KmsClient
from security_models import SignRequest, SignResponse, VerifyRequest, VerifyResponse

# Use AWS KMS as the concrete managed key service
# The client loads AWS credentials from environment variables (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)

def sign_plaintext(plaintext: str, key_id: str) -> str:
    """Signs a UTF‑8 plaintext using an RSA or ECC KMS key and returns the base64‑encoded signature.

    The function builds a SignRequest, delegates to AWS KMS (via KmsClient), and returns a JSON string.
    """
    client = KmsClient()
    request = SignRequest(KeyId=key_id, MessageType='RAW', Message=plaintext.encode('utf-8'))
    response = client.sign(request)
    normalized = SignResponse(**response)
    return normalized.Signature.decode('utf-8')


def verify_signature(signature_b64: str, plaintext: str, key_id: str) -> bool:
    """Verifies a signature produced by KMS Sign against the original plaintext.
    Returns True if verification succeeds, False otherwise.
    """
    client = KmsClient()
    # Convert base64 back to bytes for verification call
    signature_bytes = signature_b64.encode('utf-8')
    request = VerifyRequest(KeyId=key_id, Signature=signature_bytes,
                            MessageType='RAW', Message=plaintext.encode('utf-8'))
    response = client.verify(request)
    normalized = VerifyResponse(**response)
    return normalized.SignatureValid

if __name__ == "__main__":
    # Example usage (requires a KMS key with Signing capability)
    msg = "Secure note"
    key = "alias/MySigningKey"
    sig = sign_plaintext(msg, key)
    print(f"Signature: {sig}")
    print(f"Verified? {verify_signature(sig, msg, key)}")
