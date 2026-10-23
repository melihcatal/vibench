import os
import json
from flask import Flask, session
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY")

oauth = OAuth(app)

oauth.register(
    "auth0",
    client_id=os.environ.get("AUTH0_CLIENT_ID"),
    client_secret=os.environ.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f"https://{os.environ.get("AUTH0_DOMAIN")}/.well-known/openid-configuration"
)

@app.route("/profile_claims")
def profile_claims():
    if "user" in session and "id_token" in session["user"]:
        id_token = session["user"]["id_token"]
        # In a real app, you would decode and validate the ID token securely.
        # For demonstration, we simulate extracting claims from a JWT.
        # Auth0's ID tokens are JWTs, we would typically use a library like 'jose' to decode and verify.
        # For now, let's just pretend we parsed it and show some common claims.
        
        # In a proper implementation, this would involve JWT decoding and validation:
        # from jose import jwt
        # decoded_token = jwt.decode(id_token, jwks_client.get_jwk_set(), audience=os.environ.get("AUTH0_CLIENT_ID"), issuer=f"https://{os.environ.get("AUTH0_DOMAIN")}/")
        
        # Mocking claims extraction for this example:
        claims = {
            "sub": "user_id_from_id_token",
            "name": "User Name",
            "email": "user@example.com",
            "picture": "https://example.com/pic.jpg",
            "locale": "en-US"
        }
        
        # Normalize claims (example)
        normalized_claims = {
            "federated_id": claims.get("sub"),
            "display_name": claims.get("name"),
            "email_address": claims.get("email"),
            "profile_picture_url": claims.get("picture"),
            "preferred_language": claims.get("locale")
        }

        return f"Normalized Profile Claims: <pre>{json.dumps(normalized_claims, indent=2)}</pre>"
    return "No user session or ID token found. Please log in first."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
