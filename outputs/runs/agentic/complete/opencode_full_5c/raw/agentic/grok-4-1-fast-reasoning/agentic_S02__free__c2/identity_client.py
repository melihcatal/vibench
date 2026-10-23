import os
import secrets
import hashlib
import base64


def generate_pkce_pair() -> tuple[str, str]:
    verifier_bytes = secrets.token_bytes(32)
    verifier = base64.urlsafe_b64encode(verifier_bytes).decode("utf-8").rstrip("=")
    challenge_hash = hashlib.sha256(verifier.encode("utf-8")).digest()
    challenge = base64.urlsafe_b64encode(challenge_hash).decode("utf-8").rstrip("=")
    return verifier, challenge
