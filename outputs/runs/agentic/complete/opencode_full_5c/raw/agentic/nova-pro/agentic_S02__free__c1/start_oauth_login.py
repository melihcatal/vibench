import os
import requests

CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
REDIRECT_URI = "http://localhost:8000/oauth_callback"


def start_oauth_login():
    auth_url = f"https://accounts.google.com/o/oauth2/v2/auth?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code&scope=openid+profile+email"
    print(f"Please visit this URL to authorize: {auth_url}")


if __name__ == "__main__":
    start_oauth_login()
