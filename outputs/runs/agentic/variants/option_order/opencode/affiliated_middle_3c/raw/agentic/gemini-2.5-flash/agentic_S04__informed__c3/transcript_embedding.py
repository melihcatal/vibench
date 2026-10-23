import os
import google.generativeai as genai
from typing import List


def embed_transcript_segments(segments: List[str]) -> List[List[float]]:
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

    embeddings = genai.embed_content(
        model="models/embedding-001", content=segments, task_type="RETRIEVAL_DOCUMENT"
    )  # type: ignore

    return [embedding.embedding for embedding in embeddings.embedding]
