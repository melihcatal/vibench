import os
from document_client import DocumentClient
import google.generativeai as genai


def embed_document_section(text_segment: str) -> list[float]:
    client_helper = DocumentClient()
    genai_client = client_helper.get_gemini_client()

    if not os.getenv("GOOGLE_API_KEY"):
        raise ValueError(
            "GOOGLE_API_KEY environment variable must be set for Gemini Embeddings."
        )

    # Using a specific embedding model, e.g., 'models/text-embedding-004'
    # Check Gemini API documentation for available models
    result = genai_client.embed_content(
        model="models/text-embedding-004", content=text_segment
    )
    return result["embedding"]
