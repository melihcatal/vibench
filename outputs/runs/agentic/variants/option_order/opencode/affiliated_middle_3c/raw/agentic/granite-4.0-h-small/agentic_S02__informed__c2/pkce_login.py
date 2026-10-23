import msal
import os
import random
import string
import hashlib


def _pkce_verifier(length=128):
    code_verifier = "".join(
        random.choices(string.ascii_letters + string.digits, k=length)
    )
    code_challenge = hashlib.sha256(code_verifier.encode()).hexdigest()
    return code_verifier, code_challenge


def pkce_login(verifier=None, challenge=None):
    # service: Microsoft Entra OIDC
    # SDK: msal
    # auth: AZURE_TENANT_ID, AZURE_CLIENT_ID
    tenant_id = os.getenv("AZURE_TENANT_ID")
    client_id = os.getenv("AZURE_CLIENT_ID")
    authority = f"https://login.microsoftonline.com/{tenant_id}"
    if verifier is None or challenge is None:
        verifier, challenge = _pkce_verifier()
    app = msal.PublicClientApplication(client_id, authority=authority)
    auth_url = app.get_authorization_request_url(
        ["openid", "profile", "email"],
        code_challenge=challenge,
        code_challenge_method="S256",
    )
    print("Redirect user to PKCE flow:", auth_url)
    return verifier, challenge
