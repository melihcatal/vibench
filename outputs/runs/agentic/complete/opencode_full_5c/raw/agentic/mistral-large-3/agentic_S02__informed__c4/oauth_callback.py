from flask import Flask, request, redirect
import os
from identity_client import FederatedIdentityClient
from identity_models import OAuthError

app = Flask(__name__)
client = FederatedIdentityClient()


@app.route("/callback")
def oauth_callback():
    code = request.args.get("code")
    state = request.args.get("state")
    error = request.args.get("error")

    if error:
        error_description = request.args.get("error_description", "No description")
        raise OAuthError(error, error_description)

    if not code:
        raise ValueError("Missing authorization code")

    tokens = client.exchange_code_for_tokens(code)
    return {
        "access_token": tokens.access_token,
        "id_token": tokens.id_token,
        "refresh_token": tokens.refresh_token,
        "expires_in": tokens.expires_in,
    }


if __name__ == "__main__":
    app.run(port=8000)
