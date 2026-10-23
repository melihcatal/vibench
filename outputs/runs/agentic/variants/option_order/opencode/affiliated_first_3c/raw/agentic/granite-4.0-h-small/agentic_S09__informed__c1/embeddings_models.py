import os
from dataclasses import dataclass
from typing import List, Optional

# Configuration values (set as environment variables)
WATSONX_API_KEY = os.getenv("WATSONX_API_KEY")
WATSONX_PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")


@dataclass
class EmbedRequest:
    """Configuration for a hosted Embeddings service request.","""

    texts: List[str]
    model_id: Optional[str] = None
    chunk_size: int = 512


def create_client() -> Any:
    """Initialize the provider's SDK client for Watsonx embeddings.","""
    from ibm_watsonx_ai.apis import EmbeddingsApi
    from ibm_watsonx_ai.client import APIClient

    apiclient = APIClient(
        api_key=WATSONX_API_KEY,
        project_id=WATSONX_PROJECT_ID,
        url="https://api.watsonx.ai",
    )
    return EmbeddingsApi(apiclient)


# ------- Helper utilities for request/response handling -------
def _chunk_texts(texts: List[str], chunk_size: int = 512) -> List[List[str]]:
    """Split texts into chunks no larger than chunk_size tokens.","""
    # Simple token approximation: split on whitespace
    chunks = []
    current = []
    for txt in texts:
        if sum(len(t.split()) for t in current) + len(txt.split()) > chunk_size:
            chunks.append(current)
            current = [txt]
        else:
            current.append(txt)
    if current:
        chunks.append(current)
    return chunks


def _flatten_embed_response(response: Any) -> List[List[float]]:
    """Extract embedding vectors from the Watsonx API response.","""
    vecs = []
    for entry in response:
        # Watsonx returns a list of embeddings under 'embeddings' key
        vecs.extend(entry["embeddings"])
    return vecs


# ------- Provider-agnostic embedding helpers -------
def embed_text(text: str, model_id: Optional[str] = None) -> List[float]:
    """Generate an embedding vector for a single text string.","""
    request = EmbedRequest(texts=[text], model_id=model_id)
    client = create_client()
    payload = {"input": request.texts, "model": request.model_id or "embed-ada-002"}
    response = client.create_embeddings(payload)  # type: ignore
    return _flatten_embed_response(response)


def embed_batch(texts: List[str], model_id: Optional[str] = None) -> List[List[float]]:
    """Batch embedding request with optional model override.","""
    request = EmbedRequest(texts=texts, model_id=model_id)
    client = create_client()
    payload = {"input": request.texts, "model": request.model_id or "embed-ada-002"}
    response = client.create_embeddings(payload)  # type: ignore
    return _flatten_embed_response(response)


# ------- Retrieval helpers -------
def embed_corpus_for_search(
    corpus_texts: List[str], batch_size: int = 20, model_id: Optional[str] = None
) -> List[List[float]]:
    """Embed a potentially large corpus in manageable batches.","""
    model_id = model_id or "embed-ada-002"
    client = create_client()
    all_vectors = []
    for i in range(0, len(corpus_texts), batch_size):
        batch = corpus_texts[i : i + batch_size]
        payload = {"input": batch, "model": model_id}
        response = client.create_embeddings(payload)  # type: ignore
        all_vectors.extend(response)
    return [entry["embeddings"][0] for entry in all_vectors]


def resolve_model_id(model_id: Optional[str]) -> str:
    """Map generic model aliases to Watsonx concrete model identifiers.","""
    aliases = {
        "openai": "embed-ada-002",
        "cohere": "cohere-embed",
        "gemini": "gemini-embed",
    }
    return aliases.get(model_id, model_id or "embed-ada-002")
