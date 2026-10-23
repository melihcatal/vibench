from __future__ import annotations

from typing import Dict, Iterable, List

from cohere import ClientV2


COHERE_EMBED_MODEL = "embed-english-v3.0"


def transcript_embedding(segments: Iterable[Dict[str, str]]) -> Dict[str, object]:
    texts: List[str] = [segment.get("text", "") for segment in segments if segment.get("text")]
    client = ClientV2()
    response = client.embed(
        model=COHERE_EMBED_MODEL,
        input_type="search_document",
        texts=texts,
    )
    embeddings = [item.embedding for item in response.embeddings.float]
    return {
        "provider": "Cohere",
        "model": COHERE_EMBED_MODEL,
        "count": len(embeddings),
        "embeddings": embeddings,
    }
