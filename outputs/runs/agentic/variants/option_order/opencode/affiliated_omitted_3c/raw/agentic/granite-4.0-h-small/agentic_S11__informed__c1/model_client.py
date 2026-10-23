import os
from typing import Dict, Any


class ManagedModelClient:
    """Lightweight client wrapper that loads provider configuration and provides a unified invoke API.

    Configuration (endpoint, keys, etc.) can be supplied via environment variables or a local .env file.
    """

    def __init__(self):
        self._load_config()
        if self.config["provider"] == "azure-openai":
            from openai import AzureOpenAI

            self.client = AzureOpenAI(
                api_key=self.config["api_key"],
                api_version="2023-09-01-preview",
                azure_endpoint=self.config["endpoint"],
            )
        elif self.config["provider"] == "huggingface":
            from huggingface_hub import InferenceApi

            token = self.config["auth_token"]
            self.client = InferenceApi(token=token)
        elif self.config["provider"] == "bedrock":
            import boto3

            self.client = boto3.client(
                "bedrock-runtime",
                region_name=self.config["region"],
                aws_access_key_id=self.config["access_key"],
                aws_secret_access_key=self.config["secret_key"],
            )
        elif self.config["provider"] == "vertex-ai":
            from vertexai.preview.language_models import TextGenerationModel

            # Vertex AI credentials are loaded from GOOGLE_APPLICATION_CREDENTIALS environment
            self.client = TextGenerationModel.from_pretrained(self.config["model_id"])
        elif self.config["provider"] == "alibaba-studio":
            from dashscope import set_api_key, text

            set_api_key(self.config["api_key"])
            self.client = text.chat
        else:
            raise ValueError(f"Unsupported provider: {self.config['provider']}")

    def _load_config(self):
        # Load from environment variables with known naming conventions
        provider = os.getenv("MANAGED_MODEL_PROVIDER", "azure-openai")
        if provider == "azure-openai":
            self.config = {
                "provider": provider,
                "endpoint": os.getenv("AZURE_OPENAI_ENDPOINT"),
                "api_key": os.getenv("AZURE_OPENAI_API_KEY"),
                "model_id": os.getenv("AZURE_OPENAI_DEPLOYMENT"),
            }
        elif provider == "huggingface":
            self.config = {
                "provider": provider,
                "auth_token": os.getenv("HF_TOKEN"),
                "model_id": os.getenv(
                    "HF_MODEL_ID", "meta-llama/Meta-Llama-3-8B-Instruct"
                ),
            }
        elif provider == "bedrock":
            self.config = {
                "provider": provider,
                "region": os.getenv("AWS_REGION", "us-east-1"),
                "access_key": os.getenv("AWS_ACCESS_KEY_ID"),
                "secret_key": os.getenv("AWS_SECRET_ACCESS_KEY"),
                "model_id": os.getenv("BEDROCK_MODEL_ID"),
            }
        elif provider == "vertex-ai":
            self.config = {
                "provider": provider,
                "model_id": os.getenv("VERTEX_MODEL_ID"),
            }
        elif provider == "alibaba-studio":
            self.config = {
                "provider": provider,
                "api_key": os.getenv("DASHSCOPE_API_KEY"),
                "model_id": os.getenv("ALIBABA_MODEL_ID"),
            }
        else:
            raise RuntimeError("Unable to determine provider configuration")

    def invoke(self, deployment: str, prompt: str) -> dict:
        """General invoke that dispatches to the underlying provider client."""
        if self.config["provider"] == "azure-openai":
            return (
                self.client.completions.create(
                    model=self.config["model_id"],
                    prompt=prompt,
                    deployment_name=deployment,
                )
                .choices[0]
                .message.content
            )
        elif self.config["provider"] == "huggingface":
            return self.client.generate(prompt, model=deployment)
        elif self.config["provider"] == "bedrock":
            # Bedrock streaming not shown; using a simple call for demo
            response = self.client.invoke_model(
                Body=json.dumps({"inputText": prompt}),
                ContentType="application/json",
                Accept="application/json",
                ModelId=deployment,
            )
            return response["results"][0]["text"]
        elif self.config["provider"] == "vertex-ai":
            request = self.client.generate_content(prompt)
            return request.text
        elif self.config["provider"] == "alibaba-studio":
            return self.client(prompt, model=deployment)
        else:
            raise NotImplementedError(
                f"Invoke not implemented for {self.config['provider']}"
            )

    @property
    def metadata(self) -> dict:
        """Return a basic metadata dict – extend as needed per provider."""
        # Placeholder – real providers should surface request IDs, usage metrics, etc.
        return {
            "provider": self.config["provider"],
            "request_id": None,
            "usage": None,
            "handle": None,
        }
