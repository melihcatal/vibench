import os
import jwt  # Using pyjwt for ID token decoding/validation (more robust than simple base64 decode)
from flask import Flask, redirect, url_for, session, request
from identity_client import exchange_code_for_tokens, GOOGLE_CLIENT_ID
from identity_models import OAuthTokens

# Google Identity Platform OIDC integration
# Provider-identifying signal: GOOGLE_CLIENT_ID and exchange_code_for_tokens in identity_client.py

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "supersecretkey")


@app.route("/oauth/callback/google")
def oauth_callback():
    """Handles the OAuth callback from Google and exchanges the authorization code for tokens."""
    error = request.args.get("error")
    if error:
        return f"OAuth error: {error}", 400

    code = request.args.get("code")
    state = request.args.get("state")
    stored_state = session.pop("oauth_state", None)

    if not code or not state or state != stored_state:
        return "Invalid state or missing code", 400

    try:
        response = exchange_code_for_tokens(code=code)
        token_data = response.json()

        # For production, proper JWT validation is crucial.
        # Here we perform a basic decode for demonstration.
        # In a real app, you would verify signature, audience, issuer, etc.
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

        return f"Login successful! User ID (from ID Token sub claim): {id_token_payload.get('sub')}"

    except Exception as e:
        return f"Failed to exchange code for tokens: {e}", 500


if __name__ == "__main__":
    # Example usage: This endpoint is hit by Google after successful authorization.
    # You would typically set GOOGLE_REDIRECT_URI to http://127.0.0.1:5000/oauth/callback/google
    app.run(debug=True)
