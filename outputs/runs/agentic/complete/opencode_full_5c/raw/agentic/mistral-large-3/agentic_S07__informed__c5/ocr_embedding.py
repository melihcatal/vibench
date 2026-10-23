import os
from typing import List, Dict
import cohere
from .document_models import OCRResponse


def embed_text(text: str, model: str = "embed-english-v3.0") -> List[float]:
    """
    Embeds text using Cohere Embed API.
    Requires COHERE_API_KEY environment variable.
    """
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable not set")

    co = cohere.Client(api_key)
    response = co.embed(texts=[text], model=model, input_type="search_document")
    return response.embeddings[0]


def ocr_embedding(ocr_response: OCRResponse) -> Dict[str, List[float]]:
    """
    Embeds extracted document sections for semantic retrieval using Cohere API.
    """
    full_text_embedding = embed_text(ocr_response.full_text)
    block_embeddings = []
    for block in ocr_response.blocks:
        embedding = embed_text(block.text)
        block_embeddings.append(
            {
                "text": block.text,
                "bounding_box": block.bounding_box,
                "embedding": embedding,
            }
        )

    return {
        "full_text_embedding": full_text_embedding,
        "block_embeddings": block_embeddings,
    }
