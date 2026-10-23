import os
import random
import string
import webbrowser
import urllib.parse
from identity_client import FederatedIdentityClient

def generate_pkce_codes(code_challenge_method='S256'):
    """Generate PKCE code_verifier and the corresponding code_challenge."""
    verifier = ''.join(random.choices(string.ascii_letters + string.digits, k=128))
    if code_challenge_method == 'S256':
        # Compute SHA-256 and base64url encode
        import hashlib, base64
        verifier_bytes = verifier.encode('utf-8')
        hash_bytes = hashlib.sha256(verifier_bytes).digest()
        code_challenge = base64.urlsafe_b64encode(hash_bytes).rstrip(b'=').decode()
    else:
        # Plain text for 'plain' method (not recommended)
        code_challenge = verifier
    return verifier, code_challenge


def start_pkce_login(provider='auth0'):
    """Start a PKCE‑enhanced OAuth/OIDC flow for public clients."""
    client = FederatedIdentityClient(provider=provider)
    redirect_uri = client.get_redirect_uri()  # e.g., http://localhost:5000/callback
    verifier, challenge = generate_pkce_codes()
    # Build authorization URL with PKCE parameters
    auth_url = client.get_authorize_url(
        code_challenge=challenge,
        code_challenge_method='S256',
        redirect_uri=redirect_uri
    )
    print(f'Open this URL in your browser:\n{auth_url}')
    webbrowser.open(auth_url)

# Example CLI usage
# if __name__ == '__main__':
#     start_pkce_login('auth0')
