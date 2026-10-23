import msal
import os
from flask import Flask, request, redirect

def create_oauth_callback_app():
    """Create a Flask app that handles the OAuth callback and exchanges the auth code for tokens."""
    tenant_id = os.getenv("AZURE_TENANT_ID")
    client_id = os.getenv("AZURE_CLIENT_ID")
    client_secret = os.getenv("AZURE_CLIENT_SECRET")
    if not all([tenant_id, client_id, client_secret]):
        raise RuntimeError("AZURE_TENANT_ID, AZURE_CLIENT_ID and AZURE_CLIENT_SECRET must be set in the environment")

    app = Flask(__name__)

    app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY", "temporary-secret")

    @app.route("/callback")
    def callback():
        # Retrieve the authorization code from the query string
        authorization_code = request.args.get("code")
        if not authorization_code:
            return "Missing authorization code", 400

        authority = f"https://login.microsoftonline.com/{tenant_id}"
        app = msal.ConfidentialClientApplication(
            client_id=client_id,
            authority=authority,
            client_credential=client_secret,
        )

        # Exchange code for tokens (access, refresh, id token)
        result = app.acquire_token_by_authorization_code(
            authorization_code,
            scopes=["openid", "profile", "email"],
        )

        if not result.get("access_token"):
            return f"Token exchange failed: {result.get('error_description')}", 500

        # Here you would typically store the ID token / claims and start a session
        # For demonstration we just return the token payload as JSON
        import json
        return json.dumps(result, indent=2)

    return app

if __name__ == "__main__":
    app = create_oauth_callback_app()
    app.run(port=5000)
