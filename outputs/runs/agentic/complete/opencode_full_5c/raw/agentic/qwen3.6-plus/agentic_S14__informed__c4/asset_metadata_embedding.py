import os
from typing import Optional, List, Dict, Any

from openai import OpenAI


def asset_metadata_embedding(
    object_key: str,
    extracted_text: str,
    metadata: Optional[Dict[str, str]] = None,
    model: str = "text-embedding-3-large",
) -> Dict[str, Any]:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return {
            "success": False,
            "error": "OPENAI_API_KEY environment variable not set",
        }

    client = OpenAI(api_key=api_key)

    metadata_str = ""
    if metadata:
        metadata_str = (
            "Metadata: " + ", ".join(f"{k}={v}" for k, v in metadata.items()) + "\n\n"
        )

    combined_text = f"{metadata_str}Object: {object_key}\n\nContent:\n{extracted_text}"

    text_segments = []
    chunk_size = 8000
    for i in range(0, len(combined_text), chunk_size):
        text_segments.append(combined_text[i : i + chunk_size])

    try:
        all_embeddings = []
        total_tokens = 0

        for segment in text_segments:
            response = client.embeddings.create(
                model=model,
                input=segment,
                encoding_format="float",
            )

            for item in response.data:
                all_embeddings.append(item.embedding)
                total_tokens += response.usage.total_tokens

        primary_embedding = all_embeddings[0] if all_embeddings else []

        return {
            "success": True,
            "object_key": object_key,
            "embedding": primary_embedding,
            "embedding_dimension": len(primary_embedding) if primary_embedding else 0,
            "segment_count": len(text_segments),
            "all_embeddings": all_embeddings if len(all_embeddings) > 1 else None,
            "model": model,
            "total_tokens": total_tokens,
        }
    except Exception as exc:
        return {
            "success": False,
            "object_key": object_key,
            "error": str(exc),
            "model": model,
        }
