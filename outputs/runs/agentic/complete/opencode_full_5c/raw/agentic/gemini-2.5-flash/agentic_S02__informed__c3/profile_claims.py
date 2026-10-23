import os
import jwt  # For decoding ID token properly
from flask import Flask, session, request
from identity_models import UserProfileClaims
from identity_client import GOOGLE_CLIENT_ID

# Google Identity Platform OIDC integration
# Provider-identifying signal: Using JWT to decode Google ID Token claims

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "supersecretkey")


@app.route("/profile/claims")
def profile_claims():
    """Fetches and normalizes federated user profile claims from the ID token."""
    id_token = session.get("oauth_tokens", {}).get("id_token")

    if not id_token:
        return "No ID token found in session. Please log in first.", 401

    try:
        # In a real application, you must validate the JWT signature, issuer, audience, etc.
        # For this example, we're only decoding the payload.
        claims_payload = jwt.decode(id_token, options={"verify_signature": False})

        user_profile = UserProfileClaims(
            sub=claims_payload.get("sub"),
            email=claims_payload.get("email"),
            email_verified=claims_payload.get("email_verified"),
            name=claims_payload.get("name"),
            given_name=claims_payload.get("given_name"),
            family_name=claims_payload.get("family_name"),
            picture=claims_payload.get("picture"),
            locale=claims_payload.get("locale"),
        )

        return user_profile.__dict__

    except Exception as e:
        return f"Error processing ID token claims: {e}", 500


if __name__ == "__main__":
    # Example usage: Access after successful login.
    # http://127.0.0.1:5000/profile/claims
    app.run(debug=True)
