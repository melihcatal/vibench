import os
import google.generativeai as genai
from typing import List


def embed_moderation_rationales(rationales: List[str]) -> List[List[float]]:
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = "models/embedding-001"

    embeddings: List[List[float]] = []
    for rationale in rationales:
        response = genai.embed_content(model=model, content=rationale)
        embeddings.append(response["embedding"])
    return embeddings
