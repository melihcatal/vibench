import os
from typing import Any, Dict, List, Optional

from openai import AzureOpenAI, OpenAI

from embeddings_models import EmbeddingResponse, ensure_text_batch


def _provider_client() -> Any:
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    api_key = os.getenv("AZURE_OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")
    api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-01")
    if azure_endpoint and api_key:
        return AzureOpenAI(api_key=api_key, api_version=api_version, azure_endpoint=azure_endpoint)
    return OpenAI(api_key=api_key)


def default_embedding_model() -> str:
    return os.getenv("OPENAI_EMBEDDING_MODEL", os.getenv("AZURE_OPENAI_EMBEDDING_MODEL", "text-embedding-3-small"))


def embed_texts(texts: Any, model: Optional[str] = None) -> EmbeddingResponse:
    client = _provider_client()
    payload = ensure_text_batch(texts)
    model_name = model or default_embedding_model()
    response = client.embeddings.create(model=model_name, input=payload)
    embeddings = [item.embedding for item in response.data]
    return EmbeddingResponse(embeddings=embeddings, raw=response.model_dump() if hasattr(response, "model_dump") else {"data": response.data})


def embed_single_text(text: str, model: Optional[str] = None) -> List[float]:
    return embed_texts(text, model=model).embeddings[0]
