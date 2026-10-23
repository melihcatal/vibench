import base64
import hashlib
import secrets

def generate_pkce_challenge_pair() -> tuple[str, str]:
    """
    Generates a PKCE code_verifier and code_challenge pair.
    """
    code_verifier = secrets.token_urlsafe(96)  # Generate a random string for the code verifier
    
    # S256 (SHA256) code challenge method
    s256_hash = hashlib.sha256(code_verifier.encode('utf-8')).digest()
    code_challenge = base64.urlsafe_b64encode(s256_hash).decode('utf-8').replace('=', '')
    
    return code_verifier, code_challenge
