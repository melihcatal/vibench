import os
from google.cloud import vision


def get_vision_client():
    """Initializes and returns a Google Cloud Vision client."""
    # The client uses Application Default Credentials to authenticate.
    # Ensure you have authenticated with 'gcloud auth application-default login'
    # and have set the GOOGLE_APPLICATION_CREDENTIALS environment variable.
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.environ.get(
        "GOOGLE_APPLICATION_CREDENTIALS", ""
    )
    return vision.ImageAnnotatorClient()
