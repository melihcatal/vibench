import os
from google.cloud import vision


def get_document_client():
    """
    Initializes and returns a Google Cloud Vision ImageAnnotatorClient.
    Assumes that authentication is handled via Application Default Credentials
    (e.g., by running `gcloud auth application-default login`).
    """
    # Provider-specific client class
    return vision.ImageAnnotatorClient()
