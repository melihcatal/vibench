import os


def get_client_config():
    return {
        "google": {
            "client_id": os.getenv("GOOGLE_CLIENT_ID"),
            "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
            "redirect_uri": "http://localhost:8000/oauth_callback",
        },
        "github": {
            "client_id": os.getenv("GITHUB_CLIENT_ID"),
            "redirect_uri": "http://localhost:8000/pkce_callback",
        },
    }
