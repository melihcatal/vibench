import os
from typing import List
import google.generativeai as genai
from google.generativeai.types import EmbeddingDict


def translation_memory_embedding(segments: List[str]) -> List[List[float]]:
    """
    Embeds translated segments for translation-memory search using Gemini Embeddings.
    """
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    model = "models/embedding-001"

    embeddings = []
    for segment in segments:
        response: EmbeddingDict = genai.embed_content(
            model=model, content=segment, task_type="retrieval_document"
        )
        embeddings.append(response["embedding"])

    return embeddings
