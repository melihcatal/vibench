import os

def get_aws_bedrock_client_config():
    """
    Provides configuration for AWS Bedrock client.
    """
    return {
        "region_name": os.environ.get("AWS_REGION", "us-east-1"),
        "aws_access_key_id": os.environ.get("AWS_ACCESS_KEY_ID"),
        "aws_secret_access_key": os.environ.get("AWS_SECRET_ACCESS_KEY")
    }

def get_azure_openai_config():
    """
    Provides configuration for Azure OpenAI client.
    """
    return {
        "api_type": "azure",
        "api_base": os.environ.get("AZURE_OPENAI_ENDPOINT"),
        "api_version": os.environ.get("AZURE_OPENAI_API_VERSION", "2023-05-15"),
        "api_key": os.environ.get("AZURE_OPENAI_API_KEY")
    }

def get_cohere_api_key():
    """
    Provides API key for Cohere client.
    """
    return os.environ.get("COHERE_API_KEY")

def get_vertex_ai_config():
    """
    Provides configuration for Google Cloud Vertex AI client.
    """
    return {
        "project_id": os.environ.get("GOOGLE_CLOUD_PROJECT_ID"),
        "location": os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1"),
    }

def get_openai_api_key():
    """
    Provides API key for OpenAI client.
    """
    return os.environ.get("OPENAI_API_KEY")
