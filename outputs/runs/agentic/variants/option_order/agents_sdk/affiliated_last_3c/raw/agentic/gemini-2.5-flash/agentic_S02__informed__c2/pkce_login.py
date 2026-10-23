import os
import urllib.parse
import base64
import hashlib
import secrets

def generate_pkce_challenge() -> (str, str):
    """
    Generates a code_verifier and code_challenge for PKCE.
    """
    code_verifier = secrets.token_urlsafe(96) # Generate a high-entropy cryptographically random string
    
    # S256 (SHA256) code_challenge method
    s256_hash = hashlib.sha256(code_verifier.encode('utf-8')).digest()
    code_challenge = base64.urlsafe_b64encode(s256_hash).decode('utf-8').replace('=', '')
    
    return code_verifier, code_challenge

def start_pkce_login():
    """
    Starts an OAuth 2.0 PKCE Authorization Code Flow login using Auth0.
    """
    AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN")
    AUTH0_CLIENT_ID = os.environ.get("AUTH0_CLIENT_ID")
    AUTH0_CALLBACK_URL = os.environ.get("AUTH0_CALLBACK_URL")

    if not all([AUTH0_DOMAIN, AUTH0_CLIENT_ID, AUTH0_CALLBACK_URL]):
        raise ValueError("Missing Auth0 environment variables.")

    code_verifier, code_challenge = generate_pkce_challenge()

    # In a real application, you would store the code_verifier securely in the user's session
    # print(f"Store this code_verifier securely for later: {code_verifier}")

    authorize_url = f"https://{AUTH0_DOMAIN}/authorize"
    params = {
        "response_type": "code",
        "client_id": AUTH0_CLIENT_ID,
        "redirect_uri": AUTH0_CALLBACK_URL,
        "scope": "openid profile email",
        "audience": f"https://{AUTH0_DOMAIN}/api/v2/",
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
    }
    query_string = urllib.parse.urlencode(params)
    full_auth_url = f"{authorize_url}?{query_string}"

    print(f"Redirect to: {full_auth_url}")
    return full_auth_url, code_verifier # Return code_verifier for demonstration/testing

if __name__ == "__main__":
    # Example usage (in a web application, you would redirect the user)
    os.environ["AUTH0_DOMAIN"] = "YOUR_AUTH0_DOMAIN.us.auth0.com" # Replace with your Auth0 domain
    os.environ["AUTH0_CLIENT_ID"] = "YOUR_AUTH0_CLIENT_ID"       # Replace with your Auth0 Client ID
    os.environ["AUTH0_CALLBACK_URL"] = "http://localhost:8000/pkce-callback" # Replace with your callback URL
    try:
        redirect_url, verifier = start_pkce_login()
        print(f"Generated Code Verifier: {verifier}")
    except ValueError as e:
        print(f"Error: {e}")
