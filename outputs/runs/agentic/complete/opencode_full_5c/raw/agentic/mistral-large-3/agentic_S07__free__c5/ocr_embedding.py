from typing import Dict, List
import numpy as np
import requests
from sentence_transformers import SentenceTransformer
from document_models import EmbeddingResponse


def ocr_embedding(
    sections: List[str], model_name: str = "all-MiniLM-L6-v2"
) -> EmbeddingResponse:
    """Embed extracted document sections for semantic retrieval using Sentence Transformers."""
    model = SentenceTransformer(model_name)
    embeddings = model.encode(sections, convert_to_numpy=True)

    return EmbeddingResponse(embeddings=embeddings.tolist(), sections=sections)
