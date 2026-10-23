import os
from openai import OpenAI
from typing import List, Dict, Any
import numpy as np


def embed_translated_segments(segments: List[Dict[str, str]]) -> List[Dict[str, Any]]:
    """Embed translated segments for translation-memory search using OpenAI embeddings."""
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    texts = []
    for segment in segments:
        text = f"{segment.get('source', '')} ||| {segment.get('target', '')}"
        if "context" in segment:
            text = f"{segment['context']} | {text}"
        texts.append(text)

    response = client.embeddings.create(
        model="text-embedding-3-small", input=texts, encoding_format="float"
    )

    embeddings = []
    for i, embedding_data in enumerate(response.data):
        segment = segments[i]
        embeddings.append(
            {
                "source_text": segment.get("source", ""),
                "target_text": segment.get("target", ""),
                "source_language": segment.get("source_lang", ""),
                "target_language": segment.get("target_lang", ""),
                "context": segment.get("context", ""),
                "embedding": embedding_data.embedding,
                "embedding_model": "text-embedding-3-small",
                "embedding_dim": len(embedding_data.embedding),
            }
        )

    return embeddings


def search_translation_memory(
    query_text: str,
    query_language: str,
    embeddings: List[Dict[str, Any]],
    target_language: str = None,
    top_k: int = 5,
) -> List[Dict[str, Any]]:
    """Search translation memory using cosine similarity."""
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    query_response = client.embeddings.create(
        model="text-embedding-3-small", input=query_text, encoding_format="float"
    )
    query_embedding = np.array(query_response.data[0].embedding)

    results = []
    for item in embeddings:
        if target_language and item["target_language"] != target_language:
            continue

        item_embedding = np.array(item["embedding"])
        similarity = np.dot(query_embedding, item_embedding) / (
            np.linalg.norm(query_embedding) * np.linalg.norm(item_embedding)
        )

        results.append(
            {
                "source_text": item["source_text"],
                "target_text": item["target_text"],
                "source_language": item["source_language"],
                "target_language": item["target_language"],
                "similarity": float(similarity),
                "context": item["context"],
            }
        )

    results.sort(key=lambda x: x["similarity"], reverse=True)
    return results[:top_k]
