import os
from google.cloud import logging_v2
from google.oauth2 import service_account

def get_log_client():
    credentials = service_account.Credentials.from_service_account_file(
        os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "credentials.json")
    )
    return logging_v2.Client(credentials=credentials)