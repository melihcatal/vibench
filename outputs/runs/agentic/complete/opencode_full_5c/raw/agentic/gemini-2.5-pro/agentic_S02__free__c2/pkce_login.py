import os
import hashlib
import base64
from authlib.integrations.httpx_client import OAuth2Client
from identity_client import get_identity_config


def generate_pkce_challenge():
    """
    Generates a code verifier and a corresponding code challenge for PKCE.
    """
    code_verifier = base64.urlsafe_b64encode(os.urandom(40)).decode("utf-8")
    code_verifier = code_verifier.rstrip("=")

    code_challenge = hashlib.sha256(code_verifier.encode("utf-8")).digest()
    code_challenge = base64.urlsafe_b64encode(code_challenge).decode("utf-8")
    code_challenge = code_challenge.rstrip("=")

    return code_verifier, code_challenge


async def start_okta_pkce_login():
    """
    Starts an OAuth 2.0 Authorization Code flow with PKCE for Okta.
    """
    config = get_identity_config()
    client = OAuth2Client(
        client_id=config["okta_client_id"],
        scope="openid profile email",
        redirect_uri=config["redirect_uri"],
    )

    metadata_url = f"https://{config['okta_domain']}/.well-known/openid-configuration"
    await client.fetch_discovery_info(metadata_url)

    code_verifier, code_challenge = generate_pkce_challenge()

    authorization_url, state = client.create_authorization_url(
        redirect_uri=config["redirect_uri"],
        code_challenge=code_challenge,
        code_challenge_method="S256",
    )

    # In a real application, you would store the code_verifier in the user's session
    # to use it during the token exchange.
    return authorization_url, state, code_verifier
