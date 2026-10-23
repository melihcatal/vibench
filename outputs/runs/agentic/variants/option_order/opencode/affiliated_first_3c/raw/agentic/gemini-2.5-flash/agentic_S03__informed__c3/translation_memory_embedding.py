import os
import google.generativeai as genai
from typing import List


def embed_segments(segments: List[str]) -> List[List[float]]:
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

    # The embedding model to use for text embeddings.
    # See https://ai.google.dev/models/gemini
    model_name = "models/embedding-001"

    # The embed_content documentation specifies the format.
    # See https://ai.google.dev/tutorials/python_quickstart#use-the-gemini-api
    embeddings = genai.embed_content(
        model=model_name, content=segments, task_type="RETRIEVAL_DOCUMENT"
    )
    return embeddings["embedding"]
