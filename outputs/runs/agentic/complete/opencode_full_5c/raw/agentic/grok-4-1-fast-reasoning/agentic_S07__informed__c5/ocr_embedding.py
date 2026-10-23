import os
import cohere
from typing import List
from document_models import OCRText


def ocr_embedding(sections: List[OCRText]) -> List[list[float]]:
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise ValueError("Set COHERE_API_KEY")
    co = cohere.Client(api_key)
    response = co.embed(
        texts=sections, model="embed-english-v3.0", input_type="search_document"
    )
    return response.embeddings
