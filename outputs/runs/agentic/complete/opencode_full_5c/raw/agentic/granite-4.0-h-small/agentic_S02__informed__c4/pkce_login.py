import os
import random
import string
from identity_client import IdentityClient


def generate_code_verifier(length=128):
    """Generate a PKCE code verifier (RFC 7636)."""
    chars = string.ascii_letters + string.digits + "-._~"
    return "".join(random.choice(chars) for _ in range(length))


def generate_code_challenge(verifier):
    """Create SHA-256 challenge for a PKCE verifier."""
    import hashlib

    hash_bytes = hashlib.sha256(verifier.encode()).digest()
    return hashlib.sha256(hash_bytes).hexdigest()


def pkce_login():
    """Perform an OAuth/OIDC login using PKCE for public clients.
    Uses Alibaba Cloud IDaaS EIAM OIDC as the concrete provider.
    Prints the authorization URL that the user should visit.
    """
    client = IdentityClient()
    verifier = generate_code_verifier()
    challenge = generate_code_challenge(verifier)

    auth_url = (
        f"https://{client.issuer}/oidc/auth?"
        f"response_type=code&"
        f"client_id={client.client_id}&"
        f"redirect_uri={client.redirect_uri}&"
        f"scope=openid%20profile%20email&"
        f"code_challenge={challenge}&"
        f"code_challenge_method=S256&"
        f"state={client.generate_state()}"
    )
    print(
        "Redirect the user to:\n",
        auth_url,
        "\nStore the verifier for later verification.",
    )


if __name__ == "__main__":
    pkce_login()
