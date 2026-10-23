import os
from typing import List, Dict, Any
from sentence_transformers import SentenceTransformer
from document_models import TextExtractionResponse

def embed_document_sections(text_response: TextExtractionResponse) -> Dict[str, Any]:
    """Embed extracted document sections for semantic retrieval using Hugging Face Sentence Transformers."""
    model = SentenceTransformer("all-MiniLM-L6-v2")
    
    sections = [page["text"] for page in text_response.pages]
    embeddings = model.encode(sections, convert_to_tensor=True)
    
    return {
        "embeddings": embeddings.tolist(),
        "sections": sections,
        "provider": "hugging_face_sentence_transformers",
        "model": "all-MiniLM-L6-v2"
    }