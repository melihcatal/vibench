import os
import google.generativeai as genai
from typing import List


def embed_log_messages(messages: List[str]) -> List[List[float]]:
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=api_key)

    result = genai.embed_content(model="models/embedding-001", content=messages)

    return [embedding.values for embedding in result["embedding"]]
