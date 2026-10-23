import os
import google.generativeai as genai
from typing import List


def embed_transcript_segment(segment_text: str) -> List[float]:
    """Embeds transcript segments for semantic retrieval using Gemini Embeddings (embedding-001 model)."""
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=api_key)

    response = genai.embed_content(
        model="models/embedding-001",
        content=segment_text,
        task_type="RETRIEVAL_DOCUMENT",
    )
    return response["embedding"]
