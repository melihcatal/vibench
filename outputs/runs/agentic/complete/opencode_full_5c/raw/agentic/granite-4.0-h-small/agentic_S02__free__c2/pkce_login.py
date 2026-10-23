import identity_client
import identity_models


def start_pkce_flow():
    client = identity_client.get_client()
    # Generate PKCE code verifier & challenge
    verifier, challenge = identity_models.generate_pkce_pair()
    auth_url = client.authorize_url(
        redirect_uri="http://localhost:5000/oauth/callback",
        scope="openid profile email",
        code_challenge=challenge,
        code_challenge_method="S256",
    )
    print(f"Redirect user to: {auth_url}")
    # Store verifier securely for later verification
    return verifier
