import secrets
import hashlib
import base64
from flask import Flask, redirect, url_for, session, request, jsonify

from identity_client import auth0_pkce_client
from identity_models import TokenData

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)


def start_auth0_pkce_login():
    """
    Starts an OAuth 2.0 PKCE flow with Auth0.
    """
    if not auth0_pkce_client:
        raise ConnectionError("Auth0 PKCE client not configured.")

    # Create and store a code verifier
    code_verifier = secrets.token_urlsafe(64)
    session["auth0_code_verifier"] = code_verifier

    # Create a code challenge
    code_challenge = hashlib.sha256(code_verifier.encode("utf-8")).digest()
    code_challenge = base64.urlsafe_b64encode(code_challenge).rstrip(b"=").decode("utf-8")

    redirect_uri = url_for("handle_auth0_pkce_callback", _external=True)
    auth_url, _ = auth0_pkce_client.create_authorization_url(
        redirect_uri=redirect_uri,
        code_challenge=code_challenge,
        code_challenge_method="S256",
    )
    return redirect(auth_url)


def handle_auth0_pkce_callback():
    """
    Handles the callback from Auth0 and exchanges the code for a token.
    """
    code = request.args.get("code")
    code_verifier = session.pop("auth0_code_verifier", None)

    if not code or not code_verifier:
        return jsonify({"error": "Invalid callback state"}), 400

    token_response = auth0_pkce_client.fetch_token(
        code=code,
        redirect_uri=url_for("handle_auth0_pkce_callback", _external=True),
        code_verifier=code_verifier,
        grant_type="authorization_code",
    )

    token_data = TokenData(**token_response)
    return jsonify(token_data.model_dump())


@app.route("/login/auth0-pkce")
def login_auth0_pkce():
    return start_auth0_pkce_login()


@app.route("/callback/auth0-pkce")
def handle_auth0_pkce_callback():
    return handle_auth0_pkce_callback()
