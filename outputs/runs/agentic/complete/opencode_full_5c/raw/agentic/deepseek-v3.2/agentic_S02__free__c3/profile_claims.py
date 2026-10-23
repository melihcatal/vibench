import os
import json
import requests
import jwt
from flask import Flask, session, jsonify

app = Flask(__name__)


def fetch_and_normalize_profile_claims():
    access_token = session.get("access_token")

    if not access_token:
        return None

    userinfo_endpoint = "https://openidconnect.googleapis.com/v1/userinfo"

    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(userinfo_endpoint, headers=headers)

    if response.status_code != 200:
        return None

    userinfo = response.json()

    normalized_claims = {
        "sub": userinfo.get("sub"),
        "email": userinfo.get("email"),
        "email_verified": userinfo.get("email_verified", False),
        "name": userinfo.get("name"),
        "given_name": userinfo.get("given_name"),
        "family_name": userinfo.get("family_name"),
        "picture": userinfo.get("picture"),
        "locale": userinfo.get("locale"),
        "provider": "google",
    }

    id_token = session.get("id_token")
    if id_token:
        try:
            decoded_token = jwt.decode(id_token, options={"verify_signature": False})
            normalized_claims.update(
                {
                    "iss": decoded_token.get("iss"),
                    "aud": decoded_token.get("aud"),
                    "exp": decoded_token.get("exp"),
                    "iat": decoded_token.get("iat"),
                    "auth_time": decoded_token.get("auth_time"),
                }
            )
        except jwt.PyJWTError:
            pass

    return normalized_claims


@app.route("/profile")
def get_profile_claims():
    claims = fetch_and_normalize_profile_claims()

    if not claims:
        return jsonify({"error": "Failed to fetch profile claims"}), 401

    return jsonify(claims)
