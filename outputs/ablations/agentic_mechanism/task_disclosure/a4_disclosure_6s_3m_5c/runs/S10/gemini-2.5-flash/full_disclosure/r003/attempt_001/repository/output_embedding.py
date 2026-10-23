import os
import google.generativeai as genai

# Configure Google Generative AI with API key from environment variable
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def embed_text(text: str) -> list[float]:
    """
    Embeds the given text using Google's embedding model for clustering or retrieval.

    Args:
        text: The input text to embed.

    Returns:
        A list of floats representing the embedding vector.
    """
    model = "embedding-001"
    response = genai.embed_content(
        model=model,
        content=text,
        task_type="RETRIEVAL_DOCUMENT"
    )
    return response['embedding']

