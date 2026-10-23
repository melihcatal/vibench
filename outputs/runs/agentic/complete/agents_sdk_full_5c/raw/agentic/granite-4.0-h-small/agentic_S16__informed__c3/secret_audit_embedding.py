import os
from google.cloud import genai
from typing import Dict

# Google Gemini Embeddings via google-genai SDK
def create_embedding_from_secret(payload: Dict[str, str]) -> str:
    """Creates a text embedding for a secret payload using Google Gemini model.

    The function serializes the secret dictionary to JSON (without pretty printing)
    and sends it to the Gemini embeddings endpoint. The returned embedding ID is
    returned as a string for later semantic search queries.

    Args:
        payload (Dict[str, str]): The secret data as a dictionary.

    Returns:
        str: The embedding ID returned by the Gemini API.
    """
    genai.set_api_key(os.getenv('GOOGLE_API_KEY'))
    model = genai.GenerativeModel('gemini-1.5-pro-001')  # choose a model that supports embeddings
    # Gemini's embed API expects a single string input for embeddings
    text_input = json.dumps(payload, separators=(',', ':'))
    response = model.embed_content(text_input)
    # response.embeddings[0].id is the unique embedding identifier
    return response.embeddings[0].id
