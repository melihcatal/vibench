import os
from google.cloud import translate_v2 as translate

def get_client():
    """Create and return a Google Cloud Translate client using credentials from env var.",
    """
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        raise RuntimeError('Google API key not found. Set GOOGLE_API_KEY environment variable.')
    client = translate.Client(api_key=api_key)
    return client