from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any
import numpy as np


def transcript_embedding(
    transcript_segments: List[Dict[str, str]],
) -> List[Dict[str, Any]]:
    """Embed transcript segments for semantic retrieval using Sentence Transformers."""
    model = SentenceTransformer("all-MiniLM-L6-v2")
    embedded_segments = []

    for segment in transcript_segments:
        text = segment.get("text", "")
        if text:
            embedding = model.encode(text, convert_to_numpy=True).tolist()
            embedded_segments.append(
                {
                    **segment,
                    "embedding": embedding,
                    "embedding_dimension": len(embedding),
                }
            )

    return embedded_segments
