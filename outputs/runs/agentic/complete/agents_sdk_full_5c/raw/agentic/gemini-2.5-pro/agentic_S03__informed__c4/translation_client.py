import os
from google.cloud import translate_v2 as translate

def get_translation_client():
    """
    Initializes and returns a Google Cloud Translation API client.
    
    Relies on the GOOGLE_APPLICATION_CREDENTIALS environment variable for authentication.
    """
    # The client will automatically use the credentials from the environment variable.
    client = translate.Client()
    return client
