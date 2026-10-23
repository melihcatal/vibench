import os

# Centralized configuration loading
# In a real application, this might use a library like Pydantic's BaseSettings
# or a more robust configuration management system.

def get_google_api_key():
    """Returns the Google API Key for services like Vision and Perspective."""
    return os.getenv("GOOGLE_API_KEY")

def get_openai_api_key():
    """Returns the OpenAI API Key."""
    return os.getenv("OPENAI_API_KEY")

def get_aws_credentials():
    """Returns a dictionary with AWS credentials."""
    return {
        "aws_access_key_id": os.getenv("AWS_ACCESS_KEY_ID"),
        "aws_secret_access_key": os.getenv("AWS_SECRET_ACCESS_KEY"),
        "region_name": os.getenv("AWS_REGION", "us-east-1"),
    }

def get_anthropic_api_key():
    """Returns the Anthropic API Key."""
    return os.getenv("ANTHROPIC_API_KEY")

def get_deepl_api_key():
    """Returns the DeepL API Key."""
    return os.getenv("DEEPL_AUTH_KEY")

def get_azure_storage_connection_string():
    """Returns the Azure Blob Storage connection string."""
    return os.getenv("AZURE_STORAGE_CONNECTION_STRING")
