import os
import google.generativeai as genai

def embed_script(script: str) -> list[float]:
    """
    Embeds a narration script using Google's Generative AI embedding model.

    Args:
        script: The narration script to embed.

    Returns:
        A list of floats representing the embedding vector.
    """
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = "models/embedding-001"
    response = genai.embed_content(model=model, content=script)
    return response["embedding"]

