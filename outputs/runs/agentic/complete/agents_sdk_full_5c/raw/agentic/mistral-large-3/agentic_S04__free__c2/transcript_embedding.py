from sentence_transformers import SentenceTransformer
from typing import List, Optional
from pydantic import BaseModel
import numpy as np
import os

class EmbeddingRequest(BaseModel):
    segments: List[str]


class EmbeddingResponse(BaseModel):
    embeddings: Optional[List[List[float]]]
    error: Optional[str]

def transcript_embedding(segments: List[str]) -> EmbeddingResponse:
    """
    Embeds transcript segments for semantic retrieval using Hugging Face Sentence Transformers.
    """
    try:
        model = SentenceTransformer("all-MiniLM-L6-v2")
        embeddings = model.encode(segments, convert_to_numpy=True).tolist()
        return EmbeddingResponse(
            embeddings=embeddings,
            error=None
        )
    except Exception as e:
        return EmbeddingResponse(
            embeddings=None,
            error=str(e)
        )