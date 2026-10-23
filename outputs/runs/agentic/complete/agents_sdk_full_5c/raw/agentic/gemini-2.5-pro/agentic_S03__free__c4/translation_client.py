import os
from typing import Tuple

def get_google_project_id():
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")
    return project_id

def get_azure_translator_credentials() -> Tuple[str, str, str]:
    endpoint = os.getenv("AZURE_TRANSLATOR_ENDPOINT")
    api_key = os.getenv("AZURE_TRANSLATOR_KEY")
    region = os.getenv("AZURE_TRANSLATOR_REGION")
    if not all([endpoint, api_key, region]):
        raise ValueError("Azure Translator environment variables not set (ENDPOINT, KEY, REGION).")
    return endpoint, api_key, region

def get_aws_credentials() -> Tuple[str, str, str]:
    access_key = os.getenv("AWS_ACCESS_KEY_ID")
    secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    region = os.getenv("AWS_DEFAULT_REGION")
    if not all([access_key, secret_key, region]):
        raise ValueError("AWS environment variables not set (ID, KEY, REGION).")
    return access_key, secret_key, region

def get_deepl_api_key():
    api_key = os.getenv("DEEPL_AUTH_KEY")
    if not api_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")
    return api_key

def get_cohere_api_key():
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable not set.")
    return api_key
    
def get_perspective_api_key():
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")
    return api_key

def get_openai_api_key():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")
    return api_key

def get_elevenlabs_api_key():
    api_key = os.getenv("ELEVEN_API_KEY")
    if not api_key:
        raise ValueError("ELEVEN_API_KEY environment variable not set.")
    return api_key
