import os
import google.generativeai as genai
from typing import List


def embed_moderation_reason(reason_texts: List[str]) -> List[List[float]]:
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable must be set.")
    genai.configure(api_key=api_key)

    result = genai.embed_content(
        model="models/embedding-001",
        content=reason_texts,
        task_type="RETRIEVAL_DOCUMENT",
    )

    return [embedding.tolist() for embedding in result["embedding"]]
