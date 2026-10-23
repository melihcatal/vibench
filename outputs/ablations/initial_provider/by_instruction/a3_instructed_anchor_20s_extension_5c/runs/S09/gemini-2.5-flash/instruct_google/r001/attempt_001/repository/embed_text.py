import os
from typing import List

import google.generativeai as genai

def embed_text(text: str) -> List[float]:
    """Generates an embedding vector for a single text string using Google's Generative AI.

    Args:
        text: The input text string.

    Returns:
        A list of floats representing the embedding vector.
    """
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.get_model("embedding-001")
    embedding = model.embed_content(content=text)["embedding"]
    return embedding

