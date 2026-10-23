import os
import base64
import hashlib
from flask import Flask, redirect, url_for, session, request, jsonify
from identity_client import Auth0Client
from identity_models import OAuthLoginRequest, OAuthCallbackRequest, TokenResponse

app = Flask(__name__)
app.secret_key = os.environ.get(
    "FLASK_SECRET_KEY", "super-secret-key"
)  # AUTH0-specific

auth0_client = Auth0Client()


def generate_pkce_codes():
    code_verifier = (
        base64.urlsafe_b64encode(os.urandom(32)).rstrip(b"=").decode("utf-8")
    )
    code_challenge = (
        base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode("utf-8")).digest())
        .rstrip(b"=")
        .decode("utf-8")
    )
    return code_verifier, code_challenge


@app.route("/pkce-login")
def pkce_login():
    code_verifier, code_challenge = generate_pkce_codes()
    session["code_verifier"] = (
        code_verifier  # Store code verifier for later use (Auth0 specific)
    )

    req = OAuthLoginRequest(
        redirect_uri=url_for("pkce_callback", _external=True),
        scope=request.args.get("scope", "openid profile email"),
        audience=request.args.get("audience"),
    )
    state = os.urandom(16).hex()
    session["oauth_state"] = state

    authorize_url = auth0_client.get_authorize_url(
        redirect_uri=req.redirect_uri,
        scope=req.scope,
        audience=req.audience,
        state=state,
        code_challenge=code_challenge,
        code_challenge_method="S256",  # Auth0 specific
    )
    return redirect(authorize_url)


@app.route("/pkce-callback")
def pkce_callback():
    state = request.args.get("state")
    if state != session.get("oauth_state"):
        return jsonify({"error": "Invalid state parameter"}), 400
    session.pop("oauth_state", None)

    code_verifier = session.pop(
        "code_verifier", None
    )  # Retrieve and remove code verifier (Auth0 specific)
    if not code_verifier:
        return jsonify({"error": "PKCE code verifier not found in session."}), 400

    req = OAuthCallbackRequest(
        code=request.args.get("code"),
        state=state,
        redirect_uri=url_for("pkce_callback", _external=True),
    )

    try:
        token_data = auth0_client.exchange_code_for_tokens(
            req.code, req.redirect_uri, code_verifier=code_verifier
        )
        token_response = TokenResponse(**token_data)
        session["access_token"] = token_response.access_token
        session["id_token"] = token_response.id_token  # AUTH0-specific
        return jsonify(token_response.dict())
    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(port=5000)
