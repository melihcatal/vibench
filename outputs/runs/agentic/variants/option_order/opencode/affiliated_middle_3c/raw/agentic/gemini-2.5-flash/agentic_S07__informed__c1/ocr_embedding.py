import google.generativeai as genai
import os
from document_models import OCREmbedding
from typing import List


def embed_text_with_gemini(text_chunks: List[str]) -> List[OCREmbedding]:
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY must be set in environment.")
    genai.configure(api_key=api_key)

    embeddings: List[OCREmbedding] = []
    for text_chunk in text_chunks:
        response = genai.embed_content(model="models/embedding-001", content=text_chunk)
        embeddings.append(
            OCREmbedding(text=text_chunk, embedding=response["embedding"])
        )
    return embeddings
