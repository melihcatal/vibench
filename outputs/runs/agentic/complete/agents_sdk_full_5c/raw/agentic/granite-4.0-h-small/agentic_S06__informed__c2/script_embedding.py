import os
import requests
from typing import Optional, List, Dict

# Reference: Azure OpenAI Embeddings API (or the public OpenAI API)
# Provider identifier: `openai` SDK (supports Azure endpoint via `api_base`, `api_key`)
from openai import OpenAI

# Environment variables expected by the service client
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_ORG = os.getenv("OPENAI_ORG", "YOUR_ORG")
OPENAI_BASE_URL = os.getenv(
    "OPENAI_BASE_URL", "https://api.openai.com/v1"
)  # Use Azure base URL when deploying to Azure OpenAI


class ScriptEmbedding:
    """Service that embeds text scripts using an external embedding model.

    Uses the OpenAI Embeddings API for illustration; the import of `openai`
    and the usage of `OPENAI_API_KEY` make the provider explicit.
    """
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY, api_base=OPENAI_BASE_URL)

    def embed(self, script: str, model: str = "text-embedding-ada-002") -> List[float]:
        """Generate embedding for a given script.

        Returns a list of floats representing the embedding vector.
        """
        resp = self.client.embeddings.create(
            model=model,
            input=script,
            # Provider‑specific options could be added here
        )
        # The response structure: {"data": [{"embedding": [...]}]}
        return resp["data"][0]["embedding"]

    @classmethod
    def get_client(cls) -> 'ScriptEmbedding':
        if not hasattr(cls, "_instance"):
            cls._instance = cls()
        return cls._instance

# Simple helper for quick calls without instantiating the class
embed_script = ScriptEmbedding.get_client().embed
