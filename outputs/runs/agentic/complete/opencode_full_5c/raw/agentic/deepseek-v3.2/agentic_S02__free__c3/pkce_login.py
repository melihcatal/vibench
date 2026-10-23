import os
import secrets
import hashlib
import base64
import urllib.parse
from flask import Flask, redirect, session, jsonify, request

app = Flask(__name__)


def generate_pkce_code_verifier():
    return secrets.token_urlsafe(64)


def generate_pkce_code_challenge(code_verifier):
    sha256_hash = hashlib.sha256(code_verifier.encode()).digest()
    code_challenge = base64.urlsafe_b64encode(sha256_hash).decode().replace("=", "")
    return code_challenge


@app.route("/pkce-login")
def start_pkce_login():
    client_id = os.environ.get("OKTA_CLIENT_ID")
    redirect_uri = os.environ.get(
        "OKTA_REDIRECT_URI", "http://localhost:5000/pkce-callback"
    )

    code_verifier = generate_pkce_code_verifier()
    code_challenge = generate_pkce_code_challenge(code_verifier)

    state = secrets.token_urlsafe(32)
    nonce = secrets.token_urlsafe(32)

    session["pkce_code_verifier"] = code_verifier
    session["pkce_state"] = state
    session["pkce_nonce"] = nonce

    okta_domain = os.environ.get("OKTA_DOMAIN", "https://dev-123456.okta.com")

    auth_params = {
        "client_id": client_id,
        "response_type": "code",
        "scope": "openid profile email",
        "redirect_uri": redirect_uri,
        "state": state,
        "nonce": nonce,
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
        "prompt": "login",
    }

    auth_url = f"{okta_domain}/oauth2/default/v1/authorize?{urllib.parse.urlencode(auth_params)}"

    return redirect(auth_url)


@app.route("/pkce-callback")
def pkce_callback():
    code = request.args.get("code")
    state = request.args.get("state")

    if state != session.get("pkce_state"):
        return jsonify({"error": "Invalid state parameter"}), 400

    code_verifier = session.get("pkce_code_verifier")

    if not code_verifier:
        return jsonify({"error": "Missing code verifier"}), 400

    okta_domain = os.environ.get("OKTA_DOMAIN", "https://dev-123456.okta.com")
    token_endpoint = f"{okta_domain}/oauth2/default/v1/token"

    token_data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": os.environ.get(
            "OKTA_REDIRECT_URI", "http://localhost:5000/pkce-callback"
        ),
        "client_id": os.environ.get("OKTA_CLIENT_ID"),
        "code_verifier": code_verifier,
    }

    response = requests.post(token_endpoint, data=token_data)

    if response.status_code != 200:
        return jsonify(
            {"error": "PKCE token exchange failed", "details": response.text}
        ), 400

    tokens = response.json()

    session["pkce_access_token"] = tokens.get("access_token")
    session["pkce_id_token"] = tokens.get("id_token")
    session["pkce_refresh_token"] = tokens.get("refresh_token")

    return jsonify(
        {
            "access_token": tokens.get("access_token"),
            "token_type": tokens.get("token_type", "Bearer"),
            "expires_in": tokens.get("expires_in"),
            "scope": tokens.get("scope"),
            "id_token": tokens.get("id_token"),
        }
    )
