import os


def get_oidc_config():
    return {
        "issuer": os.getenv("OIDC_ISSUER", "https://accounts.google.com"),
        "authorization_endpoint": os.getenv("OIDC_AUTHORIZATION_ENDPOINT", "https://accounts.google.com/o/oauth2/v2/auth"),
        "token_endpoint": os.getenv("OIDC_TOKEN_ENDPOINT", "https://oauth2.googleapis.com/token"),
        "userinfo_endpoint": os.getenv("OIDC_USERINFO_ENDPOINT", "https://openidconnect.googleapis.com/v1/userinfo"),
        "client_id": os.getenv("OIDC_CLIENT_ID", "google-client-id"),
        "client_secret": os.getenv("OIDC_CLIENT_SECRET", ""),
        "redirect_uri": os.getenv("OIDC_REDIRECT_URI", "https://app.example.com/oauth/callback"),
        "scope": os.getenv("OIDC_SCOPE", "openid email profile"),
        "code_challenge": os.getenv("OIDC_CODE_CHALLENGE", ""),
        "code_challenge_method": os.getenv("OIDC_CODE_CHALLENGE_METHOD", "S256"),
    }


def build_redirect_uri(cfg):
    return cfg["redirect_uri"]


def token_endpoint_headers(cfg):
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    if cfg.get("issuer", "").startswith("https://accounts.google.com"):
        headers["User-Agent"] = "federated-login/google-oidc"
    return headers
