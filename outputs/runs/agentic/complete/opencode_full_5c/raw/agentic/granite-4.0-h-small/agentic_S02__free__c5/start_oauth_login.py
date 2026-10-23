import os
import requests

# Provider: Okta
OKTA_DOMAIN = os.getenv("OKTA_DOMAIN", "dev-12345.okta.com")
AUTH_SERVER = f"https://{OKTA_DOMAIN}/oauth2/default/v1/authorize"

client_id = os.getenv("OKTA_CLIENT_ID")
redirect_uri = os.getenv("OKTA_REDIRECT_URI", "http://localhost:8080/callback")


def start_oauth_login():
    params = {
        "response_type": "code",
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "scope": "openid profile email",
        "state": "random-state",
    }
    print("Visit this URL to login:")
    print(f"{AUTH_SERVER}?{requests.compat.urlencode(params)}")


if __name__ == "__main__":
    start_oauth_login()
