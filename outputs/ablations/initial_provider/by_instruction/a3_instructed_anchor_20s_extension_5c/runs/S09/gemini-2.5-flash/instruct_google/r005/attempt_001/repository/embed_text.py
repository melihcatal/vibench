import google.generativeai as genai
import os

def embed_text(text: str) -> list[float]:
    """Generates an embedding vector for a single text string using Google's Generative AI.

    Args:
        text: The input text string.

    Returns:
        A list of floats representing the embedding vector.
    """
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.get_model("models/embedding-001")
    response = model.embed_content(content=text)
    return response["embedding"]
