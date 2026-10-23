import os
from google.cloud import genai
from document_models import OcrResult

def generate_embedding(image_path: str, section_text: str) -> dict:
    """Create an embedding vector for a specific section of OCR text using Gemini Embeddings.
    Returns a dict containing the vector and metadata useful for retrieval.
    """
    # Use the environment variable GOOGLE_API_KEY to authenticate
    client = genai.Client()
    embed_model = client.embed_text_model("models/embed-text-001")
    # Embed the supplied section (could be a page, paragraph, or custom region)
    embeddings = embed_model.embed_text(content=section_text)
    # Response is a list of embedding objects; we take the first
    embedding = embeddings[0].embedding  # list of floats
    return {
        "embedding": embedding,
        "section_snippet": section_text[:120] + (
            "..." if len(section_text) > 120 else ""
        ),
        "start_char": 0,
        "end_char": len(section_text)
    }
