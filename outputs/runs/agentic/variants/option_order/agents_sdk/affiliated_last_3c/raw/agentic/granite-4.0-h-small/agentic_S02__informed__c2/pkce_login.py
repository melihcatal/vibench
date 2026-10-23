import msal
import os
import random
import string
import webbrowser

def pkce_login():
    """PKCE (Proof Key for Code Exchange) flow for public client applications."""
    # Load essential config from environment
    tenant_id = os.getenv("AZURE_TENANT_ID")
    client_id = os.getenv("AZURE_CLIENT_ID")
    if not all([tenant_id, client_id]):
        raise RuntimeError("AZURE_TENANT_ID and AZURE_CLIENT_ID must be set in the environment")

    # 1. Generate code_verifier (high entropy string) and its SHA256 hash (code_challenge)
    def random_code_verifier(length=128):
        chars = string.ascii_letters + string.digits + "-._~"
        return ''.join(random.choice(chars) for _ in range(length))
    code_verifier = random_code_verifier()
    # SHA-256 the verifier and base64‑url encode it for the challenge
    import hashlib, base64
    code_challenge = base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode()).digest())
    .rstrip(b'=')
    code_challenge = code_challenge.decode()

    # 2. Build the authorization request URL with PKCE
    authority = f"https://login.microsoftonline.com/{tenant_id}"
    scopes = ["openid", "profile", "email"]
    app = msal.PublicClientApplication(client_id, authority=authority)
    auth_uri = app.get_authorization_request_url(
        scopes,
        code_challenge=code_challenge,
        code_challenge_method="S256",
    )

    # 3. Open browser for user to sign in
    webbrowser.open(auth_uri)
    print("Open the above URL, sign in, and copy the returned authorization code.")
    auth_code = input("Enter the authorization code: ").strip()

    # 4. Exchange code for tokens using the verifier
    result = app.acquire_token_by_authorization_code(
        auth_code,
        scopes=scopes,
        code_verifier=code_verifier,
    )
    if not result.get('access_token'):
        raise RuntimeError(f"Token exchange failed: {result.get('error_description')}")

    print("Access token obtained!")
    print(f"ID token: {result.get('id_token')}")
    print(f"Access token: {result.get('access_token')[:20]}...")

if __name__ == "__main__":
    pkce_login()
