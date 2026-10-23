import os
from typing import Dict, Any

# This file provides local configuration and client helper utilities for Streaming Speech-to-Text.
# It can be used to centralize API key loading, client initialization, or common settings.

class SpeechClientConfig:
    """Manages configuration settings for various speech-to-text providers."""
    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.google_credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        self.assemblyai_api_key = os.getenv("ASSEMBLYAI_API_KEY")
        self.aws_region = os.getenv("AWS_REGION", "us-east-1")
        self.aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
        self.aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        self.azure_subscription_key = os.getenv("AZURE_CONTENT_MODERATOR_KEY")
        self.azure_endpoint = os.getenv("AZURE_CONTENT_MODERATOR_ENDPOINT")
        self.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
        self.cohere_api_key = os.getenv("COHERE_API_KEY")

    def get_openai_config(self) -> Dict[str, Any]:
        return {"api_key": self.openai_api_key}

    def get_google_config(self) -> Dict[str, Any]:
        return {"credentials_path": self.google_credentials_path}
    
    def get_assemblyai_config(self) -> Dict[str, Any]:
        return {"api_key": self.assemblyai_api_key}

    def get_aws_config(self) -> Dict[str, Any]:
        return {
            "region_name": self.aws_region,
            "aws_access_key_id": self.aws_access_key_id,
            "aws_secret_access_key": self.aws_secret_access_key,
        }

    def get_azure_content_moderator_config(self) -> Dict[str, Any]:
        return {
            "subscription_key": self.azure_subscription_key,
            "endpoint": self.azure_endpoint
        }
    
    def get_anthropic_config(self) -> Dict[str, Any]:
        return {"api_key": self.anthropic_api_key}

    def get_cohere_config(self) -> Dict[str, Any]:
        return {"api_key": self.cohere_api_key}

def get_speech_client_config() -> SpeechClientConfig:
    """Factory function to get a pre-configured SpeechClientConfig instance."""
    return SpeechClientConfig()
