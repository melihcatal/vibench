import os
from google.cloud import translate_v2 as translate

_translate_client = None

def get_translate_client():
    """Initializes and returns a Google Cloud Translation client."""
    global _translate_client
    if _translate_client is None:
        # GOOGLE_APPLICATION_CREDENTIALS environment variable should be set
        # or credentials provided implicitly by the environment.
        _translate_client = translate.Client()
    return _translate_client

# Example of how to set credentials for local testing if not using env variable
# from google.oauth2 import service_account
# def get_translate_client_with_credentials(json_path: str):
#     global _translate_client
#     if _translate_client is None:
#         credentials = service_account.Credentials.from_service_account_file(json_path)
#         _translate_client = translate.Client(credentials=credentials)
#     return _translate_client
