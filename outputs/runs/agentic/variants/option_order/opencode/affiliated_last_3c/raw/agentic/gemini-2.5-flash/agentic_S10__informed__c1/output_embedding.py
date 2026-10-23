import os
import google.generativeai as genai


def get_embedding(text: str, model: str = "models/embedding-001") -> list[float]:
    """
    Generates an embedding for the given text using Google Gemini Embeddings.
    Requires GOOGLE_API_KEY environment variable.
    """
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

    if not genai.get_default_model():
        raise ValueError("GOOGLE_API_KEY must be set and configured for Gemini API.")

    response = genai.embed_content(
        model=model, content=text, task_type="RETRIEVAL_DOCUMENT"
    )
    return response["embedding"]
