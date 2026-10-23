import os

class SafetyClientConfig:
    """Provides local configuration utilities for Text Content Safety."""

    @staticmethod
    def get_azure_content_safety_credentials():
        """Retrieves Azure AI Content Safety endpoint and key from environment variables."""
        endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
        key = os.getenv("AZURE_CONTENT_SAFETY_KEY")
        if not endpoint or not key:
            raise ValueError("Azure Content Safety credentials (AZURE_CONTENT_SAFETY_ENDPOINT, AZURE_CONTENT_SAFETY_KEY) not set in environment variables.")
        return endpoint, key

    @staticmethod
    def get_tisane_api_key():
        """Retrieves Tisane API key from environment variables."""
        api_key = os.getenv("TISANE_API_KEY")
        if not api_key:
            raise ValueError("Tisane API key (TISANE_API_KEY) not set in environment variable.")
        return api_key

    @staticmethod
    def get_aws_credentials():
        """Retrieves AWS credentials from environment variables."""
        aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
        aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        aws_region = os.getenv("AWS_REGION", "us-east-1")
        if not aws_access_key_id or not aws_secret_access_key:
            raise ValueError("AWS credentials (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY) not set in environment variables.")
        return aws_access_key_id, aws_secret_access_key, aws_region

    @staticmethod
    def get_google_api_key():
        """Retrieves Google API key from environment variables."""
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("Google API key (GOOGLE_API_KEY) not set in environment variable.")
        return api_key
