import os
import requests

AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
AUTH0_CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET")


def get_authorization_url():
    return f"https://{AUTH0_DOMAIN}/authorize?response_type=code&client_id={AUTH0_CLIENT_ID}&redirect_uri=http://localhost:3000/callback&scope=openid profile email&state=xyz"


if __name__ == "__main__":
    print(get_authorization_url())
