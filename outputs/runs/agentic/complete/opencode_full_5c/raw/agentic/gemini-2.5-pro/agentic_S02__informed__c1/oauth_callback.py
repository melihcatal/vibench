from flask import Flask, request, jsonify
from identity_client import (
    get_confidential_client,
    get_default_scopes,
    get_redirect_uri,
)
from identity_models import OAuthToken

app = Flask(__name__)


def handle_microsoft_entra_callback(authorization_code: str):
    client = get_confidential_client()
    scopes = get_default_scopes()
    redirect_uri = get_redirect_uri()

    result = client.acquire_token_by_authorization_code(
        authorization_code, scopes=scopes, redirect_uri=redirect_uri
    )

    if "error" in result:
        raise Exception(f"OAuth Error: {result.get('error_description')}")

    token_data = {
        "access_token": result["access_token"],
        "id_token": result.get("id_token"),
        "scope": result["scope"][0],
        "token_type": result["token_type"],
        "expires_in": result["expires_in"],
        "refresh_token": result.get("refresh_token"),
    }
    return OAuthToken(**token_data)


@app.route("/callback")
def callback():
    code = request.args.get("code")
    if not code:
        return "Authorization code not found.", 400

    try:
        token = handle_microsoft_entra_callback(code)
        return jsonify(token.model_dump())
    except Exception as e:
        return str(e), 500


if __name__ == "__main__":
    app.run(port=8000)
