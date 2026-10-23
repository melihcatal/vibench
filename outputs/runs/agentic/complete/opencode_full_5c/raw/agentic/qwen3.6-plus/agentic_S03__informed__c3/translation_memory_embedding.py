import os
import numpy as np
from openai import OpenAI
from translation_models import TranslationResponse


EMBEDDING_MODEL = "text-embedding-3-small"


def embed_translation_segments(
    translations: list[TranslationResponse],
    model: str = EMBEDDING_MODEL,
    dimensions: int = 1536,
) -> dict:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY environment variable is required for OpenAI Embeddings API access"
        )

    client = OpenAI(api_key=api_key)

    segments = []
    for translation in translations:
        for i, result in enumerate(translation.results):
            segments.append(
                {
                    "text": result.text,
                    "source_lang": translation.source_lang,
                    "target_lang": translation.target_lang,
                    "segment_index": i,
                }
            )

    texts_to_embed = [seg["text"] for seg in segments]

    if not texts_to_embed:
        return {
            "embeddings": [],
            "segments": [],
            "model": model,
            "total_segments": 0,
        }

    batch_size = 100
    all_embeddings = []

    for batch_start in range(0, len(texts_to_embed), batch_size):
        batch_texts = texts_to_embed[batch_start : batch_start + batch_size]
        response = client.embeddings.create(
            model=model,
            input=batch_texts,
            dimensions=dimensions,
        )
        for item in response.data:
            all_embeddings.append(item.embedding)

    embedding_array = np.array(all_embeddings, dtype=np.float32)

    enriched_segments = []
    for idx, seg in enumerate(segments):
        enriched_segments.append(
            {
                **seg,
                "embedding_index": idx,
            }
        )

    return {
        "embeddings": all_embeddings,
        "embedding_array": embedding_array,
        "segments": enriched_segments,
        "model": model,
        "dimensions": dimensions,
        "total_segments": len(segments),
        "service": "OpenAI Embeddings API",
    }


def search_translation_memory(
    query_text: str,
    memory: dict,
    top_k: int = 5,
) -> list[dict]:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY environment variable is required for OpenAI Embeddings API access"
        )

    client = OpenAI(api_key=api_key)

    query_response = client.embeddings.create(
        model=memory["model"],
        input=[query_text],
        dimensions=memory["dimensions"],
    )
    query_embedding = np.array(query_response.data[0].embedding, dtype=np.float32)

    memory_embeddings = memory["embedding_array"]

    if memory_embeddings.ndim == 1:
        memory_embeddings = memory_embeddings.reshape(1, -1)

    norms_query = np.linalg.norm(query_embedding)
    norms_memory = np.linalg.norm(memory_embeddings, axis=1)

    similarities = (memory_embeddings @ query_embedding) / (
        norms_memory * norms_query + 1e-9
    )

    top_indices = np.argsort(similarities)[::-1][:top_k]

    results = []
    for idx in top_indices:
        segment = memory["segments"][idx]
        results.append(
            {
                "text": segment["text"],
                "source_lang": segment["source_lang"],
                "target_lang": segment["target_lang"],
                "similarity_score": float(similarities[idx]),
            }
        )

    return results
