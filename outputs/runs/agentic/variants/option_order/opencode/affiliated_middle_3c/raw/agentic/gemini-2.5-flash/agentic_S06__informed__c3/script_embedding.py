import os
import google.generativeai as genai


def embed_script(text: str) -> list:
    """
    Embeds narration scripts for voice-asset search using Gemini Embeddings.
    """
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable must be set.")
    genai.configure(api_key=api_key)

    model = "models/embedding-001"
    response = genai.embed_content(model=model, content=text)
    return response["embedding"]
