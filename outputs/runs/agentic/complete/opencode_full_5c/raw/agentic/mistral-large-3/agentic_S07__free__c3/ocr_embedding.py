from typing import Dict, List
import numpy as np
from sentence_transformers import SentenceTransformer
from document_models import OCRResponse


def embed_text(text: str, model_name: str = "all-MiniLM-L6-v2") -> List[float]:
    """Embed extracted document sections using Sentence Transformers."""
    model = SentenceTransformer(model_name)
    embedding = model.encode(text, convert_to_numpy=True)
    return embedding.tolist()


def ocr_embedding(
    ocr_response: OCRResponse, section_delimiter: str = "\n"
) -> Dict[str, Dict]:
    """Embed extracted document sections for semantic retrieval."""
    sections = ocr_response.full_text.split(section_delimiter)
    section_embeddings = []

    for section in sections:
        section = section.strip()
        if section:
            embedding = embed_text(section)
            section_embeddings.append({"text": section, "embedding": embedding})

    return {
        "sections": section_embeddings,
        "provider": "sentence_transformers",
        "model": "all-MiniLM-L6-v2",
    }
