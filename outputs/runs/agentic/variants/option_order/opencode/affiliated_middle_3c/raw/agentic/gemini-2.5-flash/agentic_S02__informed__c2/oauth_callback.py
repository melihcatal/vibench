import os
from flask import Flask, redirect, url_for, session, request, jsonify
from identity_client import Auth0Client
from identity_models import OAuthCallbackRequest, TokenResponse

app = Flask(__name__)
app.secret_key = os.environ.get(
    "FLASK_SECRET_KEY", "super-secret-key"
)  # AUTH0-specific

auth0_client = Auth0Client()


@app.route("/callback")
def callback():
    state = request.args.get("state")
    if state != session.get("oauth_state"):
        return jsonify({"error": "Invalid state parameter"}), 400
    session.pop("oauth_state", None)

    req = OAuthCallbackRequest(
        code=request.args.get("code"),
        state=state,
        redirect_uri=url_for("callback", _external=True),
    )

    try:
        token_data = auth0_client.exchange_code_for_tokens(req.code, req.redirect_uri)
        token_response = TokenResponse(**token_data)
        session["access_token"] = token_response.access_token
        session["id_token"] = token_response.id_token  # AUTH0-specific
        return jsonify(token_response.dict())
    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(port=5000)
