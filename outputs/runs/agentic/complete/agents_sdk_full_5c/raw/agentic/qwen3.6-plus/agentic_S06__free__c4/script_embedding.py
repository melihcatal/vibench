"""
script_embedding.py - Embed narration scripts for voice-asset search.

Uses Azure OpenAI Service to generate text embeddings for narration scripts,
enabling semantic search across voice asset libraries.
Provider: Microsoft Azure OpenAI Service
Endpoint: https://{resource}.openai.azure.com/openai/deployments/{deployment}/embeddings
"""

import os
import requests
from typing import Optional, List, Dict, Any

from speech_models import TTSRequest


# Azure OpenAI configuration
AZURE_OPENAI_ENDPOINT = os.environ.get(
    "AZURE_OPENAI_ENDPOINT",
    "https://your-resource.openai.azure.com/",
)
AZURE_OPENAI_KEY = os.environ.get("AZURE_OPENAI_KEY", "")
AZURE_OPENAI_API_VERSION = os.environ.get("AZURE_OPENAI_API_VERSION", "2024-02-01")

# Azure OpenAI embedding model deployment
AZURE_OPENAI_EMBEDDING_MODEL = os.environ.get(
    "AZURE_OPENAI_EMBEDDING_MODEL",
    "text-embedding-ada-002",
)
AZURE_OPENAI_EMBEDDING_DEPLOYMENT = os.environ.get(
    "AZURE_OPENAI_EMBEDDING_DEPLOYMENT",
    "text-embedding-ada-002",
)


class ScriptEmbedding:
    """Container for a script's embedding vector and metadata."""

    def __init__(
        self,
        text: str,
        vector: List[float],
        model: str = "",
        dimensions: int = 0,
        metadata: Optional[Dict[str, str]] = None,
    ):
        self.text = text
        self.vector = vector
        self.model = model
        self.dimensions = dimensions
        self.metadata = metadata or {}

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "text": self.text,
            "model": self.model,
            "dimensions": self.dimensions,
            "vector_length": len(self.vector),
            "metadata": self.metadata,
        }


def embed_script(
    text: str,
    api_key: Optional[str] = None,
    endpoint: Optional[str] = None,
    deployment: Optional[str] = None,
    model: Optional[str] = None,
) -> ScriptEmbedding:
    """
    Generate an embedding vector for a narration script using Azure OpenAI.

    Uses the text-embedding-ada-002 model deployed on Azure OpenAI Service
    to create a dense vector representation of the script text for semantic
    search in a voice-asset library.

    Args:
        text: Narration script text to embed.
        api_key: Azure OpenAI API key.
        endpoint: Azure OpenAI resource endpoint.
        deployment: Model deployment name on Azure OpenAI.
        model: Model name (e.g., 'text-embedding-ada-002').

    Returns:
        ScriptEmbedding with vector and metadata.
    """
    key = api_key or AZURE_OPENAI_KEY
    base_endpoint = endpoint or AZURE_OPENAI_ENDPOINT
    deploy = deployment or AZURE_OPENAI_EMBEDDING_DEPLOYMENT
    model_name = model or AZURE_OPENAI_EMBEDDING_MODEL
    api_version = AZURE_OPENAI_API_VERSION

    if not key:
        raise ValueError("Azure OpenAI API key is required.")

    # Azure OpenAI embeddings endpoint
    embeddings_url = (
        f"{base_endpoint.rstrip('/')}/openai/deployments/{deploy}/embeddings"
    )

    headers = {
        "api-key": key,
        "Content-Type": "application/json",
    }

    body = {
        "input": text,
        "model": model_name,
    }

    params = {"api-version": api_version}

    try:
        response = requests.post(
            embeddings_url,
            headers=headers,
            json=body,
            params=params,
            timeout=30,
        )
        response.raise_for_status()

        result = response.json()
        embedding_data = result["data"][0]

        return ScriptEmbedding(
            text=text,
            vector=embedding_data["embedding"],
            model=model_name,
            dimensions=len(embedding_data["embedding"]),
        )

    except requests.exceptions.RequestException as exc:
        raise RuntimeError(f"Azure OpenAI embedding error: {exc}") from exc


def embed_scripts_batch(
    texts: List[str],
    api_key: Optional[str] = None,
    endpoint: Optional[str] = None,
    deployment: Optional[str] = None,
    model: Optional[str] = None,
) -> List[ScriptEmbedding]:
    """
    Generate embedding vectors for multiple narration scripts.

    Uses Azure OpenAI's batch embedding capability for the
    text-embedding-ada-002 model to process up to 16 texts per request.

    Args:
        texts: List of narration script texts to embed.
        api_key: Azure OpenAI API key.
        endpoint: Azure OpenAI resource endpoint.
        deployment: Model deployment name.
        model: Model name.

    Returns:
        List of ScriptEmbedding objects.
    """
    key = api_key or AZURE_OPENAI_KEY
    base_endpoint = endpoint or AZURE_OPENAI_ENDPOINT
    deploy = deployment or AZURE_OPENAI_EMBEDDING_DEPLOYMENT
    model_name = model or AZURE_OPENAI_EMBEDDING_MODEL
    api_version = AZURE_OPENAI_API_VERSION

    if not key:
        raise ValueError("Azure OpenAI API key is required.")

    embeddings_url = (
        f"{base_endpoint.rstrip('/')}/openai/deployments/{deploy}/embeddings"
    )

    headers = {
        "api-key": key,
        "Content-Type": "application/json",
    }

    # Azure OpenAI supports up to 16 inputs per embedding request
    batch_size = 16
    all_embeddings = []

    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]

        body = {
            "input": batch,
            "model": model_name,
        }

        params = {"api-version": api_version}

        response = requests.post(
            embeddings_url,
            headers=headers,
            json=body,
            params=params,
            timeout=60,
        )
        response.raise_for_status()

        result = response.json()

        for item in result["data"]:
            all_embeddings.append(ScriptEmbedding(
                text=batch[item["index"]],
                vector=item["embedding"],
                model=model_name,
                dimensions=len(item["embedding"]),
            ))

    return all_embeddings


def embed_tts_request(
    request: TTSRequest,
    api_key: Optional[str] = None,
    endpoint: Optional[str] = None,
) -> ScriptEmbedding:
    """
    Generate an embedding for a TTS request's text content.

    Args:
        request: TTSRequest to embed.
        api_key: Azure OpenAI API key.
        endpoint: Azure OpenAI resource endpoint.

    Returns:
        ScriptEmbedding with metadata including voice and locale info.
    """
    embedding = embed_script(
        text=request.text,
        api_key=api_key,
        endpoint=endpoint,
    )

    embedding.metadata = {
        "voice_name": request.voice_name,
        "locale": request.locale,
        "output_format": request.output_format,
    }

    return embedding


def cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
    """
    Compute cosine similarity between two embedding vectors.

    Args:
        vec_a: First embedding vector.
        vec_b: Second embedding vector.

    Returns:
        Cosine similarity score between 0 and 1.
    """
    dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
    magnitude_a = sum(a * a for a in vec_a) ** 0.5
    magnitude_b = sum(b * b for b in vec_b) ** 0.5

    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0

    return dot_product / (magnitude_a * magnitude_b)
