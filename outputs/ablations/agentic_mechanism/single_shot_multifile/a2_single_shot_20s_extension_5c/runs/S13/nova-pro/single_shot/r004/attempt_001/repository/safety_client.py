import os
from google.cloud import language_v1

def get_safety_client():
    client = language_v1.LanguageServiceClient()
    return client