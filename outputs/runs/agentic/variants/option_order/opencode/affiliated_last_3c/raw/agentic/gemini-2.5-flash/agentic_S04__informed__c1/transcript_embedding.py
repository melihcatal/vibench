import google.generativeai as genai
import os
from typing import List


def embed_transcript_segment(segment_text: str) -> List[float]:
    """
    Embeds transcript segments for semantic retrieval using Gemini Embeddings.
    """
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

    result = genai.embed_content(
        model="models/embedding-001",
        content=segment_text,
        task_type="RETRIEVAL_DOCUMENT",
    )
    return result["embedding"]
