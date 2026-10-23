import os
import json
import requests
from flask import Flask, request, session, jsonify

app = Flask(__name__)


@app.route("/callback")
def oauth_callback():
    code = request.args.get("code")
    state = request.args.get("state")
    error = request.args.get("error")

    if error:
        return jsonify({"error": error}), 400

    if state != session.get("oauth_state"):
        return jsonify({"error": "Invalid state parameter"}), 400

    token_endpoint = "https://oauth2.googleapis.com/token"

    token_data = {
        "code": code,
        "client_id": os.environ.get("GOOGLE_CLIENT_ID"),
        "client_secret": os.environ.get("GOOGLE_CLIENT_SECRET"),
        "redirect_uri": os.environ.get(
            "GOOGLE_REDIRECT_URI", "http://localhost:5000/callback"
        ),
        "grant_type": "authorization_code",
    }

    response = requests.post(token_endpoint, data=token_data)

    if response.status_code != 200:
        return jsonify(
            {"error": "Token exchange failed", "details": response.text}
        ), 400

    tokens = response.json()

    id_token = tokens.get("id_token")
    access_token = tokens.get("access_token")
    refresh_token = tokens.get("refresh_token")

    session["access_token"] = access_token
    session["id_token"] = id_token
    session["refresh_token"] = refresh_token

    return jsonify(
        {
            "access_token": access_token,
            "token_type": tokens.get("token_type", "Bearer"),
            "expires_in": tokens.get("expires_in"),
            "scope": tokens.get("scope"),
        }
    )
