import os
from flask import Flask, redirect, url_for, session, request
from identity_client import (
    build_authorization_url,
    generate_pkce_pair,
    exchange_code_for_tokens,
    GOOGLE_CLIENT_ID,
)
from identity_models import OAuthTokens
import jwt  # For decoding ID token properly

# Google Identity Platform OIDC integration with PKCE
# Provider-identifying signal: GOOGLE_CLIENT_ID and PKCE implementation tailored for Google Identity Platform

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "supersecretkey")


@app.route("/login/google/pkce")
def pkce_login():
    """Starts a Google OAuth PKCE login flow for public clients."""
    state = os.urandom(16).hex()
    session["oauth_state"] = state

    code_verifier, code_challenge = generate_pkce_pair()
    session["pkce_code_verifier"] = code_verifier

    scope = ["openid", "email", "profile"]
    auth_url = build_authorization_url(
        scope=scope, state=state, code_challenge=code_challenge, pkce_enabled=True
    )
    return redirect(auth_url)


@app.route("/oauth/callback/google/pkce")
def pkce_callback():
    """Handles the OAuth callback for PKCE flow and exchanges the authorization code for tokens."""
    error = request.args.get("error")
    if error:
        return f"OAuth error: {error}", 400

    code = request.args.get("code")
    state = request.args.get("state")
    stored_state = session.pop("oauth_state", None)
    code_verifier = session.pop("pkce_code_verifier", None)

    if not code or not state or state != stored_state or not code_verifier:
        return "Invalid state, missing code, or missing PKCE verifier", 400

    try:
        response = exchange_code_for_tokens(code=code, code_verifier=code_verifier)
        token_data = response.json()

        id_token_payload = jwt.decode(
            token_data["id_token"], options={"verify_signature": False}
        )

        oauth_tokens = OAuthTokens(
            access_token=token_data["access_token"],
            id_token=token_data["id_token"],
            refresh_token=token_data.get("refresh_token"),
            expires_in=token_data.get("expires_in"),
            token_type=token_data.get("token_type"),
        )

        session["oauth_tokens"] = oauth_tokens.__dict__  # Store tokens in session
        session["user_id_from_id_token"] = id_token_payload.get("sub")

        return f"PKCE Login successful! User ID (from ID Token sub claim): {id_token_payload.get('sub')}"

    except Exception as e:
        return f"Failed to exchange code for tokens in PKCE flow: {e}", 500


if __name__ == "__main__":
    # Example usage: http://127.0.0.1:5000/login/google/pkce
    app.run(debug=True)
