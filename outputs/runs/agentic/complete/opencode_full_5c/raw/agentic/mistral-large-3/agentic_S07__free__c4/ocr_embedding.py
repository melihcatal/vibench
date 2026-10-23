from typing import Dict, List
import os
from sentence_transformers import SentenceTransformer
from document_models import OCRResponse


def ocr_embedding(
    ocr_response: OCRResponse, model_name: str = "all-MiniLM-L6-v2"
) -> Dict[str, List[Dict]]:
    """Embed extracted document sections for semantic retrieval using Sentence Transformers."""
    model = SentenceTransformer(model_name)

    # Split text into sections (simplified for example)
    sections = [page.blocks[0].block_text for page in ocr_response.pages if page.blocks]
    if not sections:
        sections = [
            ocr_response.text[i : i + 500]
            for i in range(0, len(ocr_response.text), 500)
        ]

    embeddings = model.encode(sections)

    return {
        "provider": "sentence_transformers",
        "model": model_name,
        "sections": [
            {"text": section, "embedding": embedding.tolist()}
            for section, embedding in zip(sections, embeddings)
        ],
    }
