import os
import google.generativeai as genai
from typing import List


def embed_moderation_rationales(rationales: List[str]) -> List[List[float]]:
    """
    Embed moderation rationales for case retrieval using Google Gemini Embeddings.
    """
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

    model = "models/embedding-001"

    embeddings = genai.embed_content(
        model=model, content=rationales, task_type="RETRIEVAL_DOCUMENT"
    )

    return [embedding.values for embedding in embeddings["embedding"]]
