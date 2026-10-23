import os
import jwt  # AUTH0-specific
from flask import Flask, session, jsonify
from identity_client import Auth0Client
from identity_models import UserProfileClaims

app = Flask(__name__)
app.secret_key = os.environ.get(
    "FLASK_SECRET_KEY", "super-secret-key"
)  # AUTH0-specific

auth0_client = Auth0Client()


@app.route("/profile")
def profile_claims():
    access_token = session.get("access_token")
    id_token = session.get("id_token")  # AUTH0-specific

    if not access_token:
        return jsonify({"error": "No access token found, please log in."}), 401

    try:
        # Using Auth0 userinfo endpoint for profile claims
        userinfo = auth0_client.get_userinfo(access_token)

        # Optionally, decode ID token for claims (Auth0 specific)
        id_token_claims = {}
        if id_token:
            # For real applications, validate the ID token signature and nonce
            id_token_claims = jwt.decode(
                id_token, options={"verify_signature": False}
            )  # For simplicity, not verifying signature here.

        claims = UserProfileClaims(
            sub=userinfo.get("sub"),
            name=userinfo.get("name"),
            email=userinfo.get("email"),
            picture=userinfo.get("picture"),
            raw_claims={
                **userinfo,
                **id_token_claims,
            },  # Merging claims from userinfo and id_token
        )
        return jsonify(claims.dict())
    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(port=5000)
