import os


def get_config():
    return {
        "provider_id": os.getenv("GOOGLE_PROVIDER_ID"),
        "api_key": os.getenv("GOOGLE_API_KEY"),
        "client_id": os.getenv("GOOGLE_CLIENT_ID"),
        "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
        "redirect_uri": os.getenv("GOOGLE_REDIRECT_URI")
    }


def get_client():
    from google.oauth2.credentials import Credentials
    return Credentials()