import os
from typing import List

import google.generativeai as genai

def embed_batch(texts: List[str]) -> List[List[float]]:
    """Generates embeddings for a batch of text strings using Google's Generative AI.

    Args:
        texts: A list of input text strings.

    Returns:
        A list of lists of floats, where each inner list is an embedding vector.
    """
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.get_model("embedding-001")
    embeddings = model.embed_content(content=texts)
    return [item["embedding"] for item in embeddings["embeddings"]]

