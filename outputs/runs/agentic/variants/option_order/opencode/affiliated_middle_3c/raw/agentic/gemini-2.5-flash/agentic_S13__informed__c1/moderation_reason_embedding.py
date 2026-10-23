import os
import google.generativeai as genai
from typing import List


def embed_moderation_rationales(rationales: List[str]) -> List[List[float]]:
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    # Using a concrete embedding model. The default for text embedding is 'embedding-001'.
    model_name = "models/embedding-001"

    embeddings = []
    for rationale in rationales:
        response = genai.embed_content(
            model=model_name,
            content=rationale,
            task_type="RETRIEVAL_DOCUMENT",  # Specify task type for better embeddings
        )
        embeddings.append(response["embedding"])
    return embeddings
