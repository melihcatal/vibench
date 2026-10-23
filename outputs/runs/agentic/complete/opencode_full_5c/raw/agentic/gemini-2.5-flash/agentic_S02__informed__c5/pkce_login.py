import os
from flask import Flask, redirect, session, url_for, request, jsonify
from identity_client import Auth0Client

app = Flask(__name__)
app.secret_key = os.environ.get(
    "FLASK_SECRET_KEY", "super_secret_key"
)  # Replace with a strong secret key

auth0_client = Auth0Client()


@app.route("/login-pkce")
def login_pkce():
    pkce_challenge = auth0_client.generate_pkce_challenge()
    session["code_verifier"] = pkce_challenge["code_verifier"]

    state = os.urandom(16).hex()
    session["oauth_state"] = (
        state  # Reuse oauth_state for simplicity, though PKCE often mitigates need for state
    )
    authorization_url = auth0_client.get_pkce_authorization_url(
        code_challenge=pkce_challenge["code_challenge"], state=state
    )
    return redirect(authorization_url)


@app.route("/callback-pkce")
def callback_pkce():
    if "error" in request.args:
        return jsonify(
            {
                "error": request.args["error"],
                "error_description": request.args["error_description"],
            }
        ), 400

    if "code" in request.args and "state" in request.args:
        if request.args["state"] != session.get("oauth_state"):
            return "Invalid state parameter", 400

        code = request.args["code"]
        code_verifier = session.pop("code_verifier", None)

        if not code_verifier:
            return "Missing code_verifier in session", 400

        try:
            token_response = auth0_client.exchange_code_for_tokens(
                code, code_verifier=code_verifier
            )
            session["access_token"] = token_response.access_token
            session["id_token"] = token_response.id_token
            session["refresh_token"] = token_response.refresh_token
            return jsonify(
                {
                    "message": "PKCE Login successful!",
                    "access_token": token_response.access_token,
                }
            )
        except Exception as e:
            return str(e), 500
    return "Invalid PKCE callback request", 400


if __name__ == "__main__":
    # This file would typically be run as part of a larger Flask application.
    # Ensure environment variables are set:
    # export AUTH0_DOMAIN="your-auth0-domain.auth0.com"
    # export AUTH0_CLIENT_ID="your-client-id"
    # export AUTH0_CLIENT_SECRET="your-client-secret" # Still needed for token exchange, even with PKCE
    # export AUTH0_REDIRECT_URI="http://localhost:5000/callback-pkce"
    # export FLASK_SECRET_KEY="a_very_secret_key_indeed"
    # app.run(debug=True, port=5000)
    pass
