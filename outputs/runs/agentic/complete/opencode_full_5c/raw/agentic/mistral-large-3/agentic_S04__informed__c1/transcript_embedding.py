import os
from typing import List, Dict
import cohere


def embed_transcript_segments(
    transcript_segments: List[Dict[str, str]],
) -> List[Dict[str, any]]:
    co = cohere.Client(os.getenv("COHERE_API_KEY"))
    embedded_segments = []

    texts = [segment["text"] for segment in transcript_segments]
    response = co.embed(texts=texts, model="embed-english-v3.0")

    for i, segment in enumerate(transcript_segments):
        embedded_segments.append({**segment, "embedding": response.embeddings[i]})
    return embedded_segments
