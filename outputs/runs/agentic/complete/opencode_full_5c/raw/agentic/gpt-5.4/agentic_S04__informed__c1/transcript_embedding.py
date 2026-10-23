from __future__ import annotations

from typing import Dict, List

from openai import OpenAI


def transcript_embedding(segments: List[Dict[str, object]]) -> Dict[str, object]:
    client = OpenAI()
    inputs = [str(segment.get("text", "")) for segment in segments]
    response = client.embeddings.create(
        model="text-embedding-3-large",
        input=inputs,
    )
    embedded_segments = []
    for segment, item in zip(segments, response.data):
        updated = dict(segment)
        updated["embedding"] = item.embedding
        embedded_segments.append(updated)
    return {
        "provider": "OpenAI",
        "model": "text-embedding-3-large",
        "segments": embedded_segments,
    }
