
import os
import requests
import urllib.parse

# Google OAuth2 Endpoints
AUTHORIZATION_BASE_URL = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN_URL = "https://oauth2.googleapis.com/token"
USERINFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"

# Configuration from environment variables
CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")
REDIRECT_URI = "http://localhost:5000/callback" # This should match your registered redirect URI

if not CLIENT_ID or not CLIENT_SECRET:
    print("Error: GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET environment variables must be set.")
    exit(1)

# Scopes define the level of access your application is requesting.
# For example, "openid email profile" requests access to the user's ID, email, and basic profile info.
SCOPES = ["openid", "email", "profile"]

def start_oauth_login():
    """
    Constructs the Google OAuth2 authorization URL and prints it.
    The user should open this URL in a browser to initiate the login process.
    """
    params = {
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "scope": " ".join(SCOPES),
        "response_type": "code",
        "access_type": "offline", # To get a refresh token
        "prompt": "consent", # To ensure consent screen is shown
    }
    authorization_url = f"{AUTHORIZATION_BASE_URL}?{urllib.parse.urlencode(params)}"
    print(f"Please go to this URL to authorize: {authorization_url}")
    print("After authorization, Google will redirect to your REDIRECT_URI with a 'code' parameter.")
    print("You will then need to exchange this 'code' for an access token and refresh token.")

if __name__ == "__main__":
    start_oauth_login()

    # --- Placeholder for handling the redirect and token exchange ---
    # In a real application, you would have a web server (e.g., Flask, Django)
    # listening on REDIRECT_URI (e.g., http://localhost:5000/callback).
    # When Google redirects back, your server would extract the 'code' from the URL
    # and then make a POST request to TOKEN_URL to exchange it for tokens.
    #
    # Example (conceptual, requires a web framework to handle the callback):
    #
    # def handle_google_callback(authorization_code):
    #     token_params = {
    #         "client_id": CLIENT_ID,
    #         "client_secret": CLIENT_SECRET,
    #         "code": authorization_code,
    #         "redirect_uri": REDIRECT_URI,
    #         "grant_type": "authorization_code",
    #     }
    #     try:
    #         response = requests.post(TOKEN_URL, data=token_params)
    #         response.raise_for_status() # Raise an exception for HTTP errors
    #         tokens = response.json()
    #         access_token = tokens.get("access_token")
    #         refresh_token = tokens.get("refresh_token") # Only if access_type=offline and prompt=consent
    #         id_token = tokens.get("id_token") # JWT token
    #
    #         print("Successfully exchanged code for tokens!")
    #         print(f"Access Token: {access_token}")
    #         if refresh_token:
    #             print(f"Refresh Token: {refresh_token}")
    #
    #         # Optionally, fetch user info
    #         userinfo_response = requests.get(USERINFO_URL, headers={"Authorization": f"Bearer {access_token}"})
    #         userinfo_response.raise_for_status()
    #         user_info = userinfo_response.json()
    #         print(f"User Info: {user_info}")
    #
    #     except requests.exceptions.RequestException as e:
    #         print(f"Error exchanging code for tokens: {e}")
    #
    # # How you would call handle_google_callback depends on your web framework.
    # # For example, in Flask:
    # # @app.route("/callback")
    # # def callback():
    # #     code = request.args.get("code")
    # #     if code:
    # #         handle_google_callback(code)
    # #         return "Logged in successfully!"
    # #     return "Login failed."
