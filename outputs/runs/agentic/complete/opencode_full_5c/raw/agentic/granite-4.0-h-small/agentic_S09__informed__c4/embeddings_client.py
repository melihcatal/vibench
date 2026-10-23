import os

from openai import OpenAI
from typing import Literal

# Configuration mapping for providers
PROVIDER_CONFIG = {
    "OpenAI": {
        "client": OpenAI,
        "default_model": "text-embedding-3-large",
        "env_key": "OPENAI_API_KEY",
        "base_url": "https://api.openai.com/v1",
    },
    # Add other providers here if needed for other files
}


class DirectEmbeddingsClient:
    def __init__(self, service: Literal["OpenAI"]):
        config = PROVIDER_CONFIG.get(service)
        if not config:
            raise ValueError(f"Unsupported service: {service}")
        api_key = os.getenv(config["env_key"])
        if not api_key:
            raise RuntimeError(f"Missing environment variable {config['env_key']}")
        self.client = config["client"](api_key=api_key)
        # For OpenAI we can set the endpoint if using Azure, otherwise default
        self.base_url = config.get("base_url")
        if self.base_url:
            self.client.base_url = self.base_url

    def embed(self, text: str) -> list[float]:
        """Embed a single text string using the configured provider."""
        response = self.client.embeddings.create(
            model=config["default_model"], input=text
        )
        return response["data"][0]["embedding"]

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        """Embed a batch of texts."""
        response = self.client.embeddings.create(
            model=config["default_model"], input=texts
        )
        return [item["embedding"] for item in response["data"]]
