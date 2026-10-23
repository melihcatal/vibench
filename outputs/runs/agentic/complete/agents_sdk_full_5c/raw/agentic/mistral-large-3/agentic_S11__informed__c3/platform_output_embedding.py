import os
from typing import List, Optional
import cohere
from model_models import ModelOutputWithMetadata


def embed_with_cohere(
    texts: List[str],
    model: str = "embed-english-v3.0",
    api_key: Optional[str] = None,
) -> List[List[float]]:
    """
    Generate embeddings for texts using Cohere Embed API.
    
    Args:
        texts: List of input texts to embed.
        model: Cohere embedding model (e.g., "embed-english-v3.0").
        api_key: Cohere API key. Defaults to environment variable.
    
    Returns:
        List of embedding vectors.
    """
    co = cohere.Client(api_key or os.getenv("COHERE_API_KEY"))
    response = co.embed(texts=texts, model=model)
    return response.embeddings


def embed_platform_output(
    output_with_metadata: ModelOutputWithMetadata,
    model: str = "embed-english-v3.0",
    api_key: Optional[str] = None,
) -> ModelOutputWithMetadata:
    """
    Embed platform model output for evaluation or retrieval.
    
    Args:
        output_with_metadata: Model output and metadata.
        model: Cohere embedding model (e.g., "embed-english-v3.0").
        api_key: Cohere API key. Defaults to environment variable.
    
    Returns:
        ModelOutputWithMetadata with embedding and updated metadata.
    """
    embedding = embed_with_cohere([output_with_metadata.output], model=model, api_key=api_key)[0]
    
    updated_metadata = output_with_metadata.metadata.copy()
    updated_metadata["embedding"] = {
        "provider": "cohere",
        "model": model,
        "vector": embedding,
    }
    
    return ModelOutputWithMetadata(
        output=output_with_metadata.output,
        metadata=updated_metadata,
    )