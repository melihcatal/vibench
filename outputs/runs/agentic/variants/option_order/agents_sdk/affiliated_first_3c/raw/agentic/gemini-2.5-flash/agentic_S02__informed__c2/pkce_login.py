import os
import base64
import hashlib
import secrets
from flask import Flask, redirect, session, url_for, request
from authlib.integrations.flask_client import OAuth
from urllib.parse import urlencode

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY")

oauth = OAuth(app)

oauth.register(
    "auth0",
    client_id=os.environ.get("AUTH0_CLIENT_ID"),
    client_secret=os.environ.get("AUTH0_CLIENT_SECRET"), # Client secret is not typically used for public clients with PKCE, but keeping it for authlib register convenience
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f"https://{os.environ.get("AUTH0_DOMAIN")}/.well-known/openid-configuration"
)

def generate_pkce_pair():
    code_verifier = secrets.token_urlsafe(64)
    s256 = hashlib.sha256()
    s256.update(code_verifier.encode("utf-8"))
    code_challenge = base64.urlsafe_b64encode(s256.digest()).decode("utf-8").replace("=", "")
    return code_verifier, code_challenge

@app.route("/pkce_login")
def pkce_login():
    code_verifier, code_challenge = generate_pkce_pair()
    session["code_verifier"] = code_verifier

    authorize_url = oauth.auth0.authorize_url(
        redirect_uri=url_for("pkce_callback", _external=True),
        code_challenge=code_challenge,
        code_challenge_method="S256"
    )
    return redirect(authorize_url)

@app.route("/pkce_callback")
def pkce_callback():
    code_verifier = session.pop("code_verifier", None)
    if not code_verifier:
        return "Error: Code verifier missing from session.", 400

    # Authlib will automatically include code_verifier in the token exchange if it's in the session or passed directly
    try:
        token = oauth.auth0.authorize_access_token(code_verifier=code_verifier)
        session["user"] = token
        return redirect("/profile") # Redirect to a profile page or similar
    except Exception as e:
        return f"Error during PKCE callback: {e}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
