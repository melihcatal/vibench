import os

def get_azure_credentials():
    """Loads Azure Content Safety credentials from environment variables."""
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")
    if not endpoint or not key:
        raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY must be set.")
    return endpoint, key

def get_watsonx_credentials():
    """Loads IBM watsonx.ai credentials from environment variables."""
    api_key = os.getenv("WATSONX_API_KEY")
    project_id = os.getenv("WATSONX_PROJECT_ID")
    if not api_key:
        raise ValueError("WATSONX_API_KEY must be set.")
    if not project_id:
        raise ValueError("WATSONX_PROJECT_ID must be set.")
        
    credentials = {
        "apikey": api_key,
        "url": "https://us-south.ml.cloud.ibm.com" # Default URL
    }
    return credentials, project_id
    
def get_tisane_credentials():
    """Loads Tisane credentials from environment variables."""
    api_key = os.getenv("TISANE_API_KEY")
    if not api_key:
        raise ValueError("TISANE_API_KEY must be set.")
    # Tisane doesn't have a separate endpoint variable, just the key.
    return api_key, None

def get_aws_credentials():
    """Loads AWS credentials from environment variables (used by boto3)."""
    access_key = os.getenv("AWS_ACCESS_KEY_ID")
    secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    if not access_key or not secret_key:
        raise ValueError("AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY must be set.")
    # Boto3 will pick these up automatically, so we just return them for validation
    return access_key, secret_key
