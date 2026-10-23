import os
import google.generativeai as genai
from typing import List
from safety_models import EmbedRequest, EmbedResponse

def embed_moderation_reason(request: EmbedRequest, config=None) -> EmbedResponse:
    """
    Generates an embedding for moderation rationale using Google Gemini embedding model.

    Args:
        request: An EmbedRequest object containing the text to embed.
        config: Optional configuration dictionary, may contain 'api_key'.

    Returns:
        An EmbedResponse object with the generated embedding.
    """
    api_key = config.get("api_key") if config else None
    genai.configure(api_key=api_key or os.environ.get("GEMINI_API_KEY"))

    # Provider and model identifying signal: 'gemini-pro-text-embedding'
    response = genai.embed_content(
        model='models/embedding-001', # Google Gemini embedding model
        content=request.text,
        task_type="RETRIEVAL_DOCUMENT" # Suitable for embedding documents for retrieval
    )

    embedding = response['embedding']
    return EmbedResponse(embedding=embedding)
