import os
from typing import Dict, Any, Optional


class EmbeddingsClient:
    """
    A local client helper for configuring and accessing various Direct Embeddings API providers.
    This client acts as a wrapper to load credentials and provide a common interface.
    """

    def __init__(self, provider: str):
        self.provider = provider.lower()
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        config = {}
        if self.provider == "dashscope":
            config["api_key"] = os.environ.get("DASHSCOPE_API_KEY")
            if not config["api_key"]:
                raise ValueError(
                    "DASHSCOPE_API_KEY environment variable not set for DashScope."
                )
        elif self.provider == "bedrock-titan":
            config["aws_access_key_id"] = os.environ.get("AWS_ACCESS_KEY_ID")
            config["aws_secret_access_key"] = os.environ.get("AWS_SECRET_ACCESS_KEY")
            config["aws_region"] = os.environ.get("AWS_REGION", "us-east-1")
            if not config["aws_access_key_id"] or not config["aws_secret_access_key"]:
                raise ValueError(
                    "AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables not set for Bedrock Titan."
                )
        elif self.provider == "openai":
            config["api_key"] = os.environ.get("OPENAI_API_KEY")
            if not config["api_key"]:
                raise ValueError(
                    "OPENAI_API_KEY environment variable not set for OpenAI."
                )
        elif self.provider == "cohere":
            config["api_key"] = os.environ.get("COHERE_API_KEY")
            if not config["api_key"]:
                raise ValueError(
                    "COHERE_API_KEY environment variable not set for Cohere."
                )
        else:
            raise ValueError(f"Unsupported embedding provider: {self.provider}")
        return config

    def get_provider_config(self) -> Dict[str, Any]:
        return self.config

    def get_provider_name(self) -> str:
        return self.provider
