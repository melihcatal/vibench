import os
from google.cloud import vision
from google.oauth2 import service_account


def get_vision_client():
    """
    Provides a configured Google Cloud Vision client.
    Assumes GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    or credentials are configured in the environment.
    """
    if "GOOGLE_APPLICATION_CREDENTIALS" in os.environ:
        credentials_path = os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
        credentials = service_account.Credentials.from_service_account_file(
            credentials_path
        )
        return vision.ImageAnnotatorClient(credentials=credentials)
    else:
        # Fallback to default credentials if env var not set
        return vision.ImageAnnotatorClient()
