import os
from typing import Any, Dict
from google.cloud import generativeai as genai


def embed_output(
    provider: str, raw_response: Any, model_name: str = "text-bison@001"
) -> Any:
    """Create embeddings for model output using Google Vertex AI Embeddings.
    Returns the embedding vector (list of floats) and metadata.
    """
    if provider != "Hugging Face":
        raise NotImplementedError(f"Embedding not implemented for provider {provider}")
    if not os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
        raise EnvironmentError(
            "Set GOOGLE_APPLICATION_CREDENTIALS to point at your Google Cloud credentials JSON"
        )
    genai.configure(api_key=os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))
    text = raw_response.get("output", "")
    embedding = genai.Embedding(model_name).embed_content(text)
    return {
        "embedding": embedding.embedding,
        "metadata": {"model": model_name, "original_text": text},
    }
