import os
import requests

CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
REDIRECT_URI = "http://localhost:8000/oauth_callback"


def oauth_callback(code):
    token_url = "https://oauth2.googleapis.com/token"
    payload = {
        "code": code,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code",
    }
    response = requests.post(token_url, data=payload)
    tokens = response.json()
    print(tokens)


if __name__ == "__main__":
    code = input("Enter the authorization code: ")
    oauth_callback(code)
