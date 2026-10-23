import os
from flask import Flask, session, jsonify
from identity_client import Auth0Client
from identity_models import UserProfileClaims

app = Flask(__name__)
app.secret_key = os.environ.get(
    "FLASK_SECRET_KEY", "super_secret_key"
)  # Replace with a strong secret key

auth0_client = Auth0Client()


@app.route("/profile")
def profile():
    access_token = session.get("access_token")
    if not access_token:
        return "Not logged in", 401

    try:
        userinfo = auth0_client.get_userinfo(access_token)
        profile_claims = UserProfileClaims(
            sub=userinfo.get("sub"),
            name=userinfo.get("name"),
            email=userinfo.get("email"),
            email_verified=userinfo.get("email_verified"),
            picture=userinfo.get("picture"),
            raw_claims=userinfo,
        )
        return jsonify(profile_claims.__dict__)
    except Exception as e:
        return str(e), 500


if __name__ == "__main__":
    # This file would typically be run as part of a larger Flask application.
    # Ensure environment variables are set and a user has logged in to have an access_token in session.
    # export AUTH0_DOMAIN="your-auth0-domain.auth0.com"
    # export FLASK_SECRET_KEY="a_very_secret_key_indeed"
    # app.run(debug=True, port=5000)
    pass
