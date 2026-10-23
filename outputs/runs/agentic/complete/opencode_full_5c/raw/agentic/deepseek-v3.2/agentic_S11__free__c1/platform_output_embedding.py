import os
from typing import List, Dict, Any
import cohere
from model_models import PlatformResponse


def embed_platform_output(response: PlatformResponse) -> Dict[str, Any]:
    """Embed platform outputs for evaluation or retrieval using Cohere embeddings."""
    cohere_api_key = os.getenv("COHERE_API_KEY")

    if not cohere_api_key:
        raise ValueError("COHERE_API_KEY environment variable is required")

    co = cohere.Client(cohere_api_key)

    try:
        embed_response = co.embed(
            texts=[response.content],
            model="embed-english-v3.0",
            input_type="search_document",
        )

        embeddings = embed_response.embeddings[0]

        return {
            "provider": "cohere",
            "embedding_model": "embed-english-v3.0",
            "embedding_dimensions": len(embeddings),
            "embedding_sample": embeddings[:5],
            "original_model": response.model_id,
            "input_type": "search_document",
            "embedding_id": embed_response.id,
            "metadata": {
                "api_version": embed_response.meta.get("api_version"),
                "billed_units": embed_response.meta.get("billed_units"),
            },
        }

    except Exception as e:
        return {
            "provider": "cohere",
            "embedding_model": "embed-english-v3.0",
            "original_model": response.model_id,
            "embedding_status": "failed",
            "error": str(e),
        }


def batch_embed_responses(responses: List[PlatformResponse]) -> List[Dict[str, Any]]:
    """Embed multiple platform responses."""
    cohere_api_key = os.getenv("COHERE_API_KEY")

    if not cohere_api_key:
        raise ValueError("COHERE_API_KEY environment variable is required")

    co = cohere.Client(cohere_api_key)

    texts = [resp.content for resp in responses]

    try:
        embed_response = co.embed(
            texts=texts, model="embed-english-v3.0", input_type="search_document"
        )

        results = []
        for i, embedding in enumerate(embed_response.embeddings):
            results.append(
                {
                    "provider": "cohere",
                    "embedding_model": "embed-english-v3.0",
                    "embedding_dimensions": len(embedding),
                    "original_model": responses[i].model_id,
                    "embedding_id": embed_response.id,
                    "index": i,
                }
            )

        return results

    except Exception as e:
        raise RuntimeError(f"Failed to batch embed with Cohere: {str(e)}")
