import os
from google.cloud import vision_v1
from google.oauth2 import service_account


def get_vision_client():
    """Initialize and return a Google Cloud Vision client."""
    credentials_info = {
        "type": os.getenv("GOOGLE_VISION_TYPE", "service_account"),
        "project_id": os.getenv("GOOGLE_VISION_PROJECT_ID"),
        "private_key_id": os.getenv("GOOGLE_VISION_PRIVATE_KEY_ID"),
        "private_key": os.getenv("GOOGLE_VISION_PRIVATE_KEY").replace("\\n", "\n"),
        "client_email": os.getenv("GOOGLE_VISION_CLIENT_EMAIL"),
        "client_id": os.getenv("GOOGLE_VISION_CLIENT_ID"),
        "auth_uri": os.getenv(
            "GOOGLE_VISION_AUTH_URI", "https://accounts.google.com/o/oauth2/auth"
        ),
        "token_uri": os.getenv(
            "GOOGLE_VISION_TOKEN_URI", "https://oauth2.googleapis.com/token"
        ),
        "auth_provider_x509_cert_url": os.getenv(
            "GOOGLE_VISION_AUTH_PROVIDER_CERT_URL",
            "https://www.googleapis.com/oauth2/v1/certs",
        ),
        "client_x509_cert_url": os.getenv("GOOGLE_VISION_CLIENT_CERT_URL"),
    }
    credentials = service_account.Credentials.from_service_account_info(
        credentials_info
    )
    return vision_v1.ImageAnnotatorClient(credentials=credentials)
