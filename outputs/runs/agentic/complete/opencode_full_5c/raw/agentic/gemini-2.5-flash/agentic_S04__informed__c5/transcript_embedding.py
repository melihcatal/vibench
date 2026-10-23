import os
from typing import List
import google.generativeai as genai


def embed_transcript_segments(segments: List[str]) -> List[List[float]]:
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = "models/embedding-001"

    embeddings = []
    for segment in segments:
        response = genai.embed_content(
            model=model, content=segment, task_type="RETRIEVAL_DOCUMENT"
        )
        embeddings.append(response["embedding"])

    return embeddings
