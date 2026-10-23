from google.cloud import vision
import os

def get_vision_client():
    """Returns a Google Cloud Vision ImageAnnotatorClient."""
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # or pass credentials explicitly.
    # For this example, we assume GOOGLE_APPLICATION_CREDENTIALS is set
    # or implicit client initialization will work.
    return vision.ImageAnnotatorClient()

# This file is primarily for providing a configured client.
# No direct execution example needed for a helper.