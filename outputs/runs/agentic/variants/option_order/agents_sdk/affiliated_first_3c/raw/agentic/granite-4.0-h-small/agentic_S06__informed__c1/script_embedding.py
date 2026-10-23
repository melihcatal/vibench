import os
from google.cloud import genai

def embed_narration(script_text):
    """Generate an embedding vector for a narration script using Gemini Embeddings (Gemini 1.5 Pro by default).
    Args:
        script_text (str): The narration to embed.
    Returns:
        list[float]: Embedding vector as a list of floats.
    """
    # gemini-1.5-pro-001 supports embeddings
    client = genai.Client()
    model = client.embeddings("gemini-1.5-pro-001")
    response = model.embed_content(script_text)
    # response.embeddings is a list of Embeddings objects with .vector attribute
    return response.embeddings[0].vector
