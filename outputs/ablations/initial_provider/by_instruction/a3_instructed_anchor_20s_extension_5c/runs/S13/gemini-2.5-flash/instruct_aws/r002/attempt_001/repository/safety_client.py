import os

class SafetyClient:
    """
    Provides local configuration and client helper utilities for Text Content Safety.
    This is a placeholder for potential shared client setup across different providers.
    """
    def __init__(self):
        # Example: Load a general configuration or API keys if needed across multiple services
        self.default_region = os.environ.get("DEFAULT_REGION", "us-east-1")
        # In a real scenario, this might initialize clients for different providers
        # or provide methods to retrieve configured clients.

    def get_provider_config(self, provider_name: str) -> dict:
        """
        Retrieves configuration specific to a given provider.
        """
        config = {}
        if provider_name == "AWS":
            config["region_name"] = os.environ.get('AWS_REGION', self.default_region)
            config["aws_access_key_id"] = os.environ.get('AWS_ACCESS_KEY_ID')
            config["aws_secret_access_key"] = os.environ.get('AWS_SECRET_ACCESS_KEY')
        elif provider_name == "Google_Perspective":
            config["api_key"] = os.environ.get('PERSPECTIVE_API_KEY')
        elif provider_name == "Azure_Content_Moderator":
            config["endpoint"] = os.environ.get("AZURE_CONTENT_MODERATOR_ENDPOINT")
            config["subscription_key"] = os.environ.get("AZURE_CONTENT_MODERATOR_SUBSCRIPTION_KEY")
        elif provider_name == "OpenAI":
            config["api_key"] = os.environ.get("OPENAI_API_KEY")
            # Add other OpenAI specific configurations here
        # Add other providers as needed
        return config

    def get_threshold_config(self) -> dict:
        """
        Retrieves general safety threshold configurations.
        This could be loaded from a central config service or file.
        """
        # Placeholder for a more complex configuration loading mechanism
        return {
            "TOXICITY": 0.75,
            "SEVERE_TOXICITY": 0.9,
            "IDENTITY_ATTACK": 0.8,
            "INSULT": 0.8,
            "PROFANITY": 0.7,
            "THREAT": 0.95,
            "sexual": 0.85
        }
