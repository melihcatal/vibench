import os
from urllib.parse import urljoin

def get_oauth_config(provider_name: str) -> dict:
    """Loads OAuth configuration for a given provider."""
    # In a real application, this would load from a secure config store
    # For this example, we use environment variables as placeholders.
    if provider_name == "google":
        return {
            "client_id": os.environ.get("GOOGLE_CLIENT_ID", "YOUR_GOOGLE_CLIENT_ID"),
            "client_secret": os.environ.get("GOOGLE_CLIENT_SECRET", "YOUR_GOOGLE_CLIENT_SECRET"),
            "redirect_uri": os.environ.get("GOOGLE_REDIRECT_URI", "http://localhost:8000/oauth_callback"),
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "userinfo_uri": "https://www.googleapis.com/oauth2/v3/userinfo",
            "scopes": ["openid", "email", "profile"],
        }
    elif provider_name == "auth0":
        return {
            "client_id": os.environ.get("AUTH0_CLIENT_ID", "YOUR_AUTH0_CLIENT_ID"),
            "domain": os.environ.get("AUTH0_DOMAIN", "YOUR_AUTH0_DOMAIN"), # e.g., dev-abc1234.us.auth0.com
            "redirect_uri": os.environ.get("AUTH0_REDIRECT_URI", "http://localhost:8000/pkce_callback"),
            "audience": os.environ.get("AUTH0_AUDIENCE", "https://api.example.com/'), # Example audience
            "scopes": ["openid", "email", "profile"],
        }
    return {}

def build_redirect_uri(base_url: str, path: str) -> str:
    """Constructs a full redirect URI."""
    return urljoin(base_url, path)
