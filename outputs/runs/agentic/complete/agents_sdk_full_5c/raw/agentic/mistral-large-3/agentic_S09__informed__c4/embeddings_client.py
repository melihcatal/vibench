import os
from typing import Optional

import openai
from openai import AzureOpenAI, OpenAI


def get_embeddings_client() -> OpenAI:
    """
    Initialize and return an OpenAI embeddings client.
    Supports both OpenAI and Azure OpenAI.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    api_version = os.getenv("OPENAI_API_VERSION", "2023-05-15")

    if azure_endpoint:
        return AzureOpenAI(
            api_key=api_key,
            azure_endpoint=azure_endpoint,
            api_version=api_version,
        )
    else:
        return OpenAI(api_key=api_key)


def get_embedding_model() -> str:
    """Return the concrete OpenAI embedding model identifier."""
    return os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")