import os

class GoogleOAuthConfig:
    CLIENT_ID = os.getenv("GOOGLE_OAUTH_CLIENT_ID")
    CLIENT_SECRET = os.getenv("GOOGLE_OAUTH_CLIENT_SECRET")
    REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI", "http://localhost:3000/callback")
    AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
    TOKEN_URL = "https://oauth2.googleapis.com/token"
    USERINFO_URL = "https://openidconnect.googleapis.com/v1/userinfo"