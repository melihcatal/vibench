import os
import google.generativeai as genai
from typing import List, Dict


def embed_translated_segments(segments: List[str]) -> List[Dict[str, Any]]:
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")
    genai.configure(api_key=api_key)

    result = genai.embed_content(model="models/embedding-001", content=segments)
    return result["embedding"]
