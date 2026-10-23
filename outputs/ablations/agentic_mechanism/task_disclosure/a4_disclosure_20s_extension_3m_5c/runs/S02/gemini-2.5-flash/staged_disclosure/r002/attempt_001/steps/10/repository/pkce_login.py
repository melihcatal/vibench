import base64
import hashlib
import os
import secrets
import webbrowser
from urllib.parse import urlencode, urlparse, parse_qs

# Replace with your Auth0 domain and client ID
AUTH0_DOMAIN = "YOUR_AUTH0_DOMAIN.auth0.com"
AUTH0_CLIENT_ID = "YOUR_AUTH0_CLIENT_ID"
AUTH0_CALLBACK_URL = "http://localhost:8080/callback"
AUTH0_AUDIENCE = "YOUR_API_AUDIENCE" # Optional, if you have an API

def generate_pkce_codes():
    """Generates a PKCE code verifier and code challenge."""
    code_verifier = secrets.token_urlsafe(64)
    code_challenge = (
        base64.urlsafe_b64encode(
            hashlib.sha256(code_verifier.encode("utf-8")).digest()
        )
        .decode("utf-8")
        .rstrip("=")
    )
    return code_verifier, code_challenge

def get_authorization_url(code_challenge):
    """Constructs the Auth0 authorization URL."""
    params = {
        "response_type": "code",
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
        "client_id": AUTH0_CLIENT_ID,
        "redirect_uri": AUTH0_CALLBACK_URL,
        "scope": "openid profile email",
        "audience": AUTH0_AUDIENCE,
    }
    return f"https://{AUTH0_DOMAIN}/authorize?{urlencode(params)}"

def exchange_code_for_token(code, code_verifier):
    """Simulates exchanging the authorization code for an access token."""
    # In a real application, you would make an HTTP POST request to Auth0's /oauth/token endpoint.
    # This is a placeholder for demonstration purposes.
    print("\n--- Simulating Token Exchange ---")
    print(f"Auth0 Token Endpoint: https://{AUTH0_DOMAIN}/oauth/token")
    print("Payload:")
    print(f"  grant_type: authorization_code")
    print(f"  client_id: {AUTH0_CLIENT_ID}")
    print(f"  code_verifier: {code_verifier}")
    print(f"  code: {code}")
    print(f"  redirect_uri: {AUTH0_CALLBACK_URL}")
    print("\n--- Token Exchange Simulated ---")
    print("If this were a real exchange, you would receive an access_token, id_token, and refresh_token.")
    print("You would then validate and use these tokens.")
    return {"access_token": "mock_access_token", "id_token": "mock_id_token"}

def main():
    code_verifier, code_challenge = generate_pkce_codes()
    auth_url = get_authorization_url(code_challenge)

    print(f"Please open this URL in your browser to log in:\n{auth_url}")
    # In a real scenario, you'd typically open this automatically:
    # webbrowser.open(auth_url)

    # For this example, we'll manually ask for the redirected URL
    redirected_url = input("\nEnter the full URL after successful login redirection: ")

    parsed_url = urlparse(redirected_url)
    query_params = parse_qs(parsed_url.query)

    if "code" in query_params:
        auth_code = query_params["code"][0]
        print(f"Received authorization code: {auth_code}")

        tokens = exchange_code_for_token(auth_code, code_verifier)
        print("\nLogin successful!")
        print(f"Access Token: {tokens.get('access_token', 'N/A')}")
        print(f"ID Token: {tokens.get('id_token', 'N/A')}")
    elif "error" in query_params:
        print(f"Error during login: {query_params['error'][0]}")
        if "error_description" in query_params:
            print(f"Description: {query_params['error_description'][0]}")
    else:
        print("No authorization code or error found in the redirected URL.")

if __name__ == "__main__":
    main()
