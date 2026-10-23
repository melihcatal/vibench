# Local configuration and client utilities for hosted LLM inference
import os


class ModelClient:
    """Utility class to configure and instantiate clients for hosted LLMs."""

    def __init__(self):
        # Set provider based on environment variable
        self.provider = os.getenv("LLM_PROVIDER", "dashscope")  # default to DashScope
        self.config = self._load_config()

    def _load_config(self) -> dict:
        """Load provider-specific API keys from environment."""
        cfg = {}
        if self.provider == "dashscope":
            cfg["api_key"] = os.getenv("DASHSCOPE_API_KEY")
        elif self.provider == "mistral":
            cfg["api_key"] = os.getenv("MISTRAL_API_KEY")
        elif self.provider == "anthropic":
            cfg["api_key"] = os.getenv("ANTHROPIC_API_KEY")
        elif self.provider == "gemini":
            cfg["api_key"] = os.getenv("GOOGLE_API_KEY")
        elif self.provider == "bedrock":
            cfg["aws_access_key"] = os.getenv("AWS_ACCESS_KEY_ID")
            cfg["aws_secret_key"] = os.getenv("AWS_SECRET_ACCESS_KEY")
        elif self.provider == "openai":
            cfg["api_key"] = os.getenv("OPENAI_API_KEY")
        elif self.provider == "watsonx":
            cfg["api_key"] = os.getenv("WATSONX_API_KEY")
            cfg["project_id"] = os.getenv("WATSONX_PROJECT_ID")
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")
        return cfg

    def get_client(self):
        """Return a configured client instance for the selected provider."""
        if self.provider == "dashscope":
            import dashscope

            return dashscope.Client(api_key=self.config["api_key"])
        elif self.provider == "mistral":
            import mistralai

            return mistralai.Clients(secret_key=self.config["api_key"])
        elif self.provider == "anthropic":
            import anthropic

            return anthropic.Anthropic(api_key=self.config["api_key"])
        elif self.provider == "gemini":
            import google.generativeai as genai

            return genai
        elif self.provider == "bedrock":
            import boto3

            return boto3.client(
                "bedrock-runtime",
                aws_access_key_id=self.config["aws_access_key"],
                aws_secret_access_key=self.config["aws_secret_key"],
            )
        elif self.provider == "openai":
            import openai

            return openai
        elif self.provider == "watsonx":
            import ibm_watsonx_ai

            return ibm_watsonx_ai.IBMClient(
                api_key=self.config["api_key"],
                project_id=self.config["project_id"],
            )
        else:
            raise NotImplementedError(f"Client for {self.provider} not implemented")
