import os
import google.generativeai as genai
from typing import List


def transcript_embedding(text_segment: str) -> List[float]:
    """
    Embeds transcript segments for semantic retrieval using Google Generative AI.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set")

    genai.configure(api_key=api_key)

    result = genai.embed_content(
        model="models/embedding-001",
        content=text_segment,
        task_type="RETRIEVAL_DOCUMENT",
    )

    return result["embedding"]
