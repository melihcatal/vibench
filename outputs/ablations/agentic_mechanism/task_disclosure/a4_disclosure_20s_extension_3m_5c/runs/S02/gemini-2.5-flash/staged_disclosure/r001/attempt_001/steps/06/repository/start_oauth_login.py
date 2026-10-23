from flask import Flask, redirect, url_for, request
import os

app = Flask(__name__)

# Replace with your actual client ID and secret
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", "YOUR_GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", "YOUR_GOOGLE_CLIENT_SECRET")
GOOGLE_AUTHORIZATION_BASE_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token" # For demonstration purposes, not used in this specific "start" script

# This should match the Authorized Redirect URIs in your Google Cloud Console
REDIRECT_URI = "http://127.0.0.1:5000/callback" 

@app.route("/")
def index():
    return "<a href=\"/login\">Log in with Google</a>"

@app.route("/login")
def login():
    # Parameters for Google OAuth 2.0 authorization code flow
    params = {
        "response_type": "code",
        "client_id": GOOGLE_CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "scope": "openid email profile", # Requesting OpenID Connect scopes
        "access_type": "offline", # To get a refresh token
        "prompt": "consent", # To ensure the consent screen is shown
    }
    
    # Construct the authorization URL
    auth_url = f"{GOOGLE_AUTHORIZATION_BASE_URL}?" + "&".join([f"{k}={v}" for k, v in params.items()])
    
    return redirect(auth_url)

@app.route("/callback")
def callback():
    # This is the endpoint where Google redirects after user authorization
    # The authorization code will be in the 'code' query parameter
    code = request.args.get("code")
    
    if code:
        return f"Authorization code received: {code}<br>This is where you would exchange the code for an access token."
    else:
        error = request.args.get("error")
        return f"Error during OAuth: {error}"

if __name__ == "__main__":
    app.run(debug=True)
