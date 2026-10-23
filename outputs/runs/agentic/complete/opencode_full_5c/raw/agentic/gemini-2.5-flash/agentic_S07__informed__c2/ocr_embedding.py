import os
from typing import List

import google.generativeai as genai


def embed_document_sections(text_sections: List[str]) -> List[List[float]]:
    """Embeds extracted document sections for semantic retrieval using Gemini Embeddings.

    Args:
        text_sections: A list of text sections to embed.

    Returns:
        A list of embedding vectors, where each vector corresponds to a text section.
    """
    # Ensure GOOGLE_API_KEY environment variable is set for authentication
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

    model = "models/embedding-001"

    embeddings: List[List[float]] = []

    for section in text_sections:
        response = genai.embed_content(model=model, content=section)
        embeddings.append(response["embedding"])

    return embeddings
