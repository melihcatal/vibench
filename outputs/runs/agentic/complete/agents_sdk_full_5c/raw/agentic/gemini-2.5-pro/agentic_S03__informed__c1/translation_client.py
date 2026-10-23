"""
Provide local configuration and client helper utilities for General Text Translation.
This implementation uses Google Cloud Translation.
"""
import os
from functools import lru_cache
from google.cloud import translate_v2 as translate

@lru_cache(maxsize=1)
def get_translation_client():
    """
    Initializes and returns a Google Cloud Translation client.
    
    Relies on GOOGLE_APPLICATION_CREDENTIALS environment variable for authentication.
    """
    if "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ:
        print("Warning: GOOGLE_APPLICATION_CREDENTIALS environment variable not set.")
        # The client will try to find default credentials.
    
    return translate.Client()

def get_project_id():
    """
    Retrieves the Google Cloud project ID from the environment.
    """
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable must be set.")
    return project_id
