import google.generativeai as genai
import os
from typing import List


def embed_text_sections(text_sections: List[str]) -> List[List[float]]:
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")
    genai.configure(api_key=api_key)

    model = "models/embedding-001"

    embeddings = []
    for text in text_sections:
        response = genai.embed_content(model=model, content=text)
        embeddings.append(response["embedding"])

    return embeddings
