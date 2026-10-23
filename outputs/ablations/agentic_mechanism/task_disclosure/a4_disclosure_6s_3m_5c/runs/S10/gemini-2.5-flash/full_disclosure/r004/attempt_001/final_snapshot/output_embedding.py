import os
import google.generativeai as genai

def embed_text(text: str) -> list[float]:
    """
    Embeds the given text using Google's generative AI embedding model.

    Args:
        text: The text to embed.

    Returns:
        A list of floats representing the embedding vector.
    """
    # Ensure that GOOGLE_API_KEY is set in the environment variables
    # For local development, you might set it like:
    # export GOOGLE_API_KEY="YOUR_API_KEY"
    if "GOOGLE_API_KEY" not in os.environ:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

    model = "models/embedding-001"
    response = genai.embed_content(model=model, content=text)
    return response["embedding"]

