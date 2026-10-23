import os
from flask import Flask, redirect, url_for, request, session, jsonify
from identity_client import Auth0Client
from identity_models import Auth0TokenResponse

app = Flask(__name__)
app.secret_key = os.environ.get(
    "FLASK_SECRET_KEY", "super_secret_key"
)  # Replace with a strong secret key

auth0_client = Auth0Client()


@app.route("/callback")
def callback():
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
        try:
            token_response: Auth0TokenResponse = auth0_client.exchange_code_for_tokens(
                code
            )
            session["access_token"] = token_response.access_token
            session["id_token"] = token_response.id_token
            session["refresh_token"] = token_response.refresh_token
            return jsonify(
                {
                    "message": "Login successful!",
                    "access_token": token_response.access_token,
                }
            )
        except Exception as e:
            return str(e), 500
    return "Invalid callback request", 400


if __name__ == "__main__":
    # This file would typically be run as part of a larger Flask application.
    # Ensure environment variables are set:
    # export AUTH0_DOMAIN="your-auth0-domain.auth0.com"
    # export AUTH0_CLIENT_ID="your-client-id"
    # export AUTH0_CLIENT_SECRET="your-client-secret"
    # export AUTH0_REDIRECT_URI="http://localhost:5000/callback"
    # export FLASK_SECRET_KEY="a_very_secret_key_indeed"
    # app.run(debug=True, port=5000)
    pass
