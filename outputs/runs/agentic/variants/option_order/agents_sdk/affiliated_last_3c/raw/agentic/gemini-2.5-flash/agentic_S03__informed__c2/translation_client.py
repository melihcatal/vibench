import os
from google.cloud import translate_v2 as translate

def get_translation_client():
    """Provides a configured Google Cloud Translation client."""
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    if not os.getenv('GOOGLE_APPLICATION_CREDENTIALS'):
        print("Warning: GOOGLE_APPLICATION_CREDENTIALS environment variable not set.")
        print("Please set it to the path of your service account key file.")
    return translate.Client()

def get_nmt_model_id():
    """Returns the model ID for Neural Machine Translation."""
    # Google Cloud Translation uses 'nmt' as a specific model identifier for NMT
    return 'nmt'
