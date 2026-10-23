import os


class Auth0Config:
    DOMAIN = os.getenv("AUTH0_DOMAIN")
    CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
    CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET")
    CALLBACK_URL = os.getenv("AUTH0_CALLBACK_URL")
    AUDIENCE = os.getenv("AUTH0_AUDIENCE")
    SCOPE = "openid profile email"
