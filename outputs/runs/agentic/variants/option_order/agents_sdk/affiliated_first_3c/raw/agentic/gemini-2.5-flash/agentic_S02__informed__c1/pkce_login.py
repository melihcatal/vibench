import os
import base64
import hashlib
import secrets
from flask import Flask, redirect, url_for, session, request
import google.auth.transport.requests
from google_auth_oauthlib.flow import Flow
from google.oauth2 import id_token

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "supersecretkey")

CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
REDIRECT_URI = os.environ.get("GOOGLE_REDIRECT_URI_PKCE", "http://localhost:5000/pkce_callback")

SCOPES = [
    "openid",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
]

def generate_pkce_codes():
    code_verifier = secrets.token_urlsafe(96)  # 128 characters, 96 bytes
    hashed = hashlib.sha256(code_verifier.encode("utf-8")).digest()
    code_challenge = base64.urlsafe_b64encode(hashed).decode("utf-8").replace("=", "")
    return code_verifier, code_challenge

@app.route("/pkce_login")
def pkce_login():
    code_verifier, code_challenge = generate_pkce_codes()
    session["code_verifier"] = code_verifier

    # Google Identity Platform requires a client_secret for most flows, but for PKCE with public clients
    # the client_secret is not used for the authorization endpoint, only client_id.
    # The client_secret.json is still typically used to initialize the Flow object in `google_auth_oauthlib`
    # even if the secret itself isn't sent in the auth request for public clients.
    flow = Flow.from_client_secrets_file(
        "client_secret.json",
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI
    )

    authorization_url, state = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true",
        code_challenge=code_challenge,
        code_challenge_method="S256"
    )

    session["state"] = state
    return redirect(authorization_url)

@app.route("/pkce_callback")
def pkce_callback():
    state = session.pop("state", None)
    code_verifier = session.pop("code_verifier", None)

    if not state or not code_verifier:
        return "<p>PKCE state or code verifier missing from session.</p>", 400

    flow = Flow.from_client_secrets_file(
        "client_secret.json",
        scopes=SCOPES,
        state=state,
        redirect_uri=REDIRECT_URI
    )

    # When exchanging the code, the code_verifier must be sent
    flow.fetch_token(
        authorization_response=request.url,
        code_verifier=code_verifier
    )

    credentials = flow.credentials

    id_info = id_token.verify_oauth2_token(
        credentials.id_token, google.auth.transport.requests.Request(), CLIENT_ID
    )

    session["credentials_pkce"] = {
        "token": credentials.token,
        "refresh_token": credentials.refresh_token,
        "token_uri": credentials.token_uri,
        "client_id": credentials.client_id,
        "scopes": credentials.scopes,
        "id_token": credentials.id_token,
        "user_info": id_info
    }

    return f"<h1>PKCE Login Successful!</h1><pre>{id_info}</pre>"

if __name__ == "__main__":
    if not os.path.exists("client_secret.json"):
        with open("client_secret.json", "w") as f:
            f.write(f'''{
                "web": {
                    "client_id": "{CLIENT_ID}",
                    "project_id": "your-pkce-project-id",
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                    "client_secret": "", # Client secret is not used for public clients with PKCE
                    "redirect_uris": ["{REDIRECT_URI}"]
                }
            }'''.format(CLIENT_ID=os.environ.get("GOOGLE_CLIENT_ID", "dummy_pkce_client_id"), REDIRECT_URI=os.environ.get("GOOGLE_REDIRECT_URI_PKCE", "http://localhost:5000/pkce_callback")))
    app.run(debug=True)
