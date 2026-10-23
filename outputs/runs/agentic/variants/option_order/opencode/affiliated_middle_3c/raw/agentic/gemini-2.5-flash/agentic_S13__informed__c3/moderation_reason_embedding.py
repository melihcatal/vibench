import os
import google.generativeai as genai
from typing import List


def embed_moderation_reason(reason_text: str) -> List[float]:
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
    # Using embedding-001 for text embeddings
    response = genai.embed_content(model="models/embedding-001", content=reason_text)
    return response["embedding"]
