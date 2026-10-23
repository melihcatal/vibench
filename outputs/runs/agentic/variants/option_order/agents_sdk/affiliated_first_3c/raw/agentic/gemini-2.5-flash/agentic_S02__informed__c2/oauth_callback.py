import os
from flask import Flask, redirect, url_for, session
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

@app.route("/callback")
def callback():
    try:
        token = oauth.auth0.authorize_access_token()
        session["user"] = token
        return redirect("/profile")
    except Exception as e:
        return f"Error during callback: {e}"

@app.route("/profile")
def profile():
    if "user" in session:
        # In a real application, you'd decode and verify the ID token here
        # For simplicity, we're just displaying the raw token data
        return f"User Profile: {session['user']}"
    return redirect("/login")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
