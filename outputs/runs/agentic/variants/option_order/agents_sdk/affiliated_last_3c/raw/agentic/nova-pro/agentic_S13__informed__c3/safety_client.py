import os

PERSPECTIVE_API_KEY = os.getenv('PERSPECTIVE_API_KEY')
TISANE_API_KEY = os.getenv('TISANE_API_KEY')
WATSONX_API_KEY = os.getenv('WATSONX_API_KEY')
WATSONX_PROJECT_ID = os.getenv('WATSONX_PROJECT_ID')
AZURE_CONTENT_SAFETY_ENDPOINT = os.getenv('AZURE_CONTENT_SAFETY_ENDPOINT')
AZURE_CONTENT_SAFETY_KEY = os.getenv('AZURE_CONTENT_SAFETY_KEY')

def get_perspective_api_key():
    return PERSPECTIVE_API_KEY

def get_tisane_api_key():
    return TISANE_API_KEY

def get_watsonx_api_key():
    return WATSONX_API_KEY

def get_watsonx_project_id():
    return WATSONX_PROJECT_ID

def get_azure_content_safety_endpoint():
    return AZURE_CONTENT_SAFETY_ENDPOINT

def get_azure_content_safety_key():
    return AZURE_CONTENT_SAFETY_KEY