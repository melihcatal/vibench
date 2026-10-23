import uuid
from typing import Tuple

# Simple PKCE implementation (public client flow)

def generate_code_verifier() -> str:
    """Create a high-entropy random string suitable for the PKCE code_verifier."""
    return uuid.uuid4().hex


def generate_challenge(verifier: str) -> str:
    """
    Generate the S256 challenge (SHA-256) required by the PKCE flow.
    Returns the Base64url encoded challenge.
    """
    import hashlib, base64
    verifier_bytes = verifier.encode('utf-8')
    hash_bytes = hashlib.sha256(verifier_bytes).digest()
    challenge = base64.urlsafe_b64encode(hash_bytes).rstrip(b'=').decode('ascii')
    return challenge

# Example usage for a CLI tool
if __name__ == '__main__':
    verifier = generate_code_verifier()
    challenge = generate_challenge(verifier)
    print('PKCE verifier:', verifier)
    print('PKCE challenge:', challenge)

# End of pkce_login.py