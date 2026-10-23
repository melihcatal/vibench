import os

# Load provider-specific credentials from environment variables
class ModelClientConfig:
    """Configuration holder for hosted LLM inference providers."""

    def __init__(self):
        # DashScope Qwen client auth via env var
        self.dashscope_api_key = os.getenv("DASHSCOPE_API_KEY")
        # Additional providers can be added here (Mistral, Anthropic, Gemini, etc.)

    def select_client(self, provider: str) -> object:
        """Return an instantiated SDK client for the given provider.

        Supported values: "dashscope", "mistral", "anthropic", "gemini", "bedrock", "openai", "watsonx"
        """
        if provider == "dashscope":
            from dashscope import chat
            return chat  # dashscope.chat.completions.create(...)
        elif provider == "mistral":
            from mistralai.rest import MistralsChatClient
            client = MistralsChatClient(base_url="https://api.mistral.ai")
            client.api_key = self.mistral_api_key  # expect MISTRAL_API_KEY env var
            return client
        elif provider == "anthropic":
            from anthropic import Client
            return Client(api_key=os.getenv("ANTHROPIC_API_KEY"))
        elif provider == "gemini":
            from google.generativeai import GenerativeModel
            return GenerativeModel(
                model_name="gemini-1.5-pro",
                use_google_application_credentials=True,
                api_key=os.getenv("GOOGLE_API_KEY")
            )
        elif provider == "bedrock":
            import boto3
            return boto3.client(
                "bedrock-runtime",
                region_name="us-east-1",
                aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
                aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
            )
        elif provider == "openai":
            import openai
            return openai
        elif provider == "watsonx":
            from ibm_watsonx_ai.services import Bedrock
            return Bedrock(
                api_key=os.getenv("WATSONX_API_KEY"),
                project_id=os.getenv("WATSONX_PROJECT_ID")
            )
        else:
            raise ValueError(f"Unsupported provider: {provider}")

# Singleton instance
model_client_config = ModelClientConfig()
