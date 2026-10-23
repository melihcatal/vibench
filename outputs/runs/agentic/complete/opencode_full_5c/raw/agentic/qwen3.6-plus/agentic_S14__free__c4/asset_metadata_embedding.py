import os
from typing import Optional, List, Dict, Any
from openai import OpenAI
from storage_models import EmbeddingRequest, EmbeddingResponse, normalize_metadata_keys


OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")


def embed_object_metadata(request: EmbeddingRequest) -> EmbeddingResponse:
    if not request.text or not request.text.strip():
        return EmbeddingResponse(
            success=False,
            model_used=request.model,
            error_message="Input text is empty",
        )

    if not OPENAI_API_KEY:
        return EmbeddingResponse(
            success=False,
            model_used=request.model,
            error_message="OPENAI_API_KEY environment variable is not set",
        )

    client = OpenAI(api_key=OPENAI_API_KEY)

    text_to_embed = request.text

    if request.metadata:
        normalized_meta = normalize_metadata_keys(request.metadata)
        meta_parts = [f"{k}: {v}" for k, v in normalized_meta.items()]
        if meta_parts:
            text_to_embed = (
                f"Metadata: {', '.join(meta_parts)}\n\nContent: {request.text}"
            )

    embedding_kwargs: Dict[str, Any] = {
        "model": "text-embedding-3-small",
        "input": text_to_embed,
    }

    if request.dimensions:
        embedding_kwargs["dimensions"] = request.dimensions

    try:
        response = client.embeddings.create(**embedding_kwargs)

        embedding = response.data[0].embedding
        model_used = response.model
        dimensions = len(embedding)

        result_metadata: Dict[str, Any] = {
            "model": model_used,
            "dimensions": dimensions,
        }

        if request.metadata:
            result_metadata["source_metadata"] = normalize_metadata_keys(
                request.metadata
            )

        if response.usage:
            result_metadata["prompt_tokens"] = response.usage.prompt_tokens

        return EmbeddingResponse(
            success=True,
            embedding=embedding,
            model_used=model_used,
            dimensions=dimensions,
            metadata=result_metadata,
        )
    except Exception as e:
        return EmbeddingResponse(
            success=False,
            model_used="text-embedding-3-small",
            error_message=f"OpenAI text-embedding-3-small embedding failed: {str(e)}",
        )


def embed_text(
    text: str,
    metadata: Optional[Dict[str, str]] = None,
    dimensions: Optional[int] = None,
) -> EmbeddingResponse:
    request = EmbeddingRequest(
        text=text,
        metadata=metadata,
        model="text-embedding-3-small",
        dimensions=dimensions,
    )
    return embed_object_metadata(request)
