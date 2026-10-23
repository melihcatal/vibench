import os
from typing import List
from observability_models import EmbedRequest, EmbedResponse
from observability_client import get_embedding_client


def embed_messages(messages: List[str]) -> EmbedResponse:
    """Embed a list of log messages for semantic retrieval using Google Gemini Embeddings.

    The concrete provider used is Google Gemini Embeddings (google-genai SDK).
    """
    client = get_embedding_client()
    resp: EmbedResponse = client.embed_content(
        contents=messages, model="gemini-1.5-pro"
    )
    return resp


# Helper to create the Gemini embeddings client – uses GOOGLE_API_KEY
def get_embedding_client():
    from google.generativeai import generative_ai

    generative_ai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    return generative_ai
