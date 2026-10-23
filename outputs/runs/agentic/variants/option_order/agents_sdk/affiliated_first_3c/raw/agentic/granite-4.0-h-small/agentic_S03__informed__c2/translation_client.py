import os
from typing import Optional, Dict, Any

# Example: set GOOGLE_APPLICATION_CREDENTIALS=path/to/key.json
GOOGLE_APPLICATION_CREDENTIALS = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

if not GOOGLE_APPLICATION_CREDENTIALS:
    raise RuntimeError('Please set GOOGLE_APPLICATION_CREDENTIALS environment variable to your Google Cloud key.')

def get_translate_client() -> Any:
    """Return a configured Google Cloud Translation client."""
    from google.cloud import translate_v2 as translate
    return translate.Client()