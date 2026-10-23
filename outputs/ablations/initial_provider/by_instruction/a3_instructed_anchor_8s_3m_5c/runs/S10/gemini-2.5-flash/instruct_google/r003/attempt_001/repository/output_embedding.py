import os
import google.generativeai as genai
from typing import List

def get_text_embedding(text: str) -> List[float]:
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")
    genai.configure(api_key=api_key)

    # Using the embedding-001 model for text embeddings
    response = genai.embed_content(model="models/embedding-001", content=text)
    return response['embedding']
