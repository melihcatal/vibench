import os

AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
AUTH0_CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI", "http://localhost:8080/callback")

if AUTH0_DOMAIN:
    AUTH_URL = f"https://{AUTH0_DOMAIN}/authorize"
    TOKEN_URL = f"https://{AUTH0_DOMAIN}/oauth/token"
    USERINFO_URL = f"https://{AUTH0_DOMAIN}/userinfo"
else:
    AUTH_URL = None
    TOKEN_URL = None
    USERINFO_URL = None