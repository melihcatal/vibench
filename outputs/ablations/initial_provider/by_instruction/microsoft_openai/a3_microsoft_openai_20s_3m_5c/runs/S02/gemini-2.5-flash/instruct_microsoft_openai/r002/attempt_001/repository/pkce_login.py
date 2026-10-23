import os
import identity_client
import oauth_callback

def start_pkce_login():
    """Initiates a PKCE login flow and returns the authorization URL and code verifier."""
    code_verifier, code_challenge = identity_client.generate_pkce_codes()
    auth_url = identity_client.build_auth_url(
        scopes=identity_client.AZURE_AD_SCOPES,
        code_challenge=code_challenge,
        code_challenge_method="S256"
    )
    print(f"Please visit this URL for PKCE login: {auth_url}")
    # In a real application, you would store the code_verifier in a session
    # associated with the user's browser until the callback is received.
    print(f"Keep this code verifier safe for the callback: {code_verifier}")
    return auth_url, code_verifier

def handle_pkce_callback(authorization_code: str, pkce_code_verifier: str):
    """Handles the PKCE callback and exchanges the authorization code using the code verifier."""
    print("Attempting to exchange authorization code with PKCE code verifier...")
    tokens = oauth_callback.handle_oauth_callback(authorization_code, pkce_code_verifier)
    if tokens:
        print("PKCE login successful!")
        print(f"Access Token (first 20 chars): {tokens.access_token[:20]}...")
        return tokens
    else:
        print("PKCE login failed.")
        return None

if __name__ == "__main__":
    print("To initiate a PKCE flow:")
    auth_url, verifier = start_pkce_login()
    print("\nOnce you complete the login in your browser, you will be redirected to the redirect URI.")
    print("Extract the 'code' query parameter from the URL and then call handle_pkce_callback.")
    print("For example:")
    print("    # Simulate a callback: assume you got the code from the redirect URL")
    print("    # received_auth_code = os.environ.get(\"PKCE_AUTH_CODE\")")
    print("    # received_code_verifier = \"YOUR_SAVED_CODE_VERIFIER_FROM_START_PKCE_LOGIN_CALL\"")
    print("    # if received_auth_code and received_code_verifier:")
    print("    #     handle_pkce_callback(received_auth_code, received_code_verifier)")
