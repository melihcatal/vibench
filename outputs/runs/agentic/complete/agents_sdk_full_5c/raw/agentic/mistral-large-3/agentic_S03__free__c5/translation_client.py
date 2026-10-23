import os
from google.cloud import translate_v2 as translate
from google.api_core.client_options import ClientOptions

def get_translation_client():
    """Initialize and return a Google Cloud Translation client."""
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "credentials.json")
    return translate.Client.from_service_account_json(credentials_path)

def get_client_with_retry():
    """Initialize a client with retry configuration."""
    client_options = ClientOptions(
        retry= {
            "initial_retry_delay": 1.0,
            "max_retry_delay": 60.0,
            "retry_delay_multiplier": 2.0,
            "total_timeout": 600.0
        }
    )
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "credentials.json")
    return translate.Client.from_service_account_json(credentials_path, client_options=client_options)