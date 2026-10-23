import os
from typing import List
import google.generativeai as genai


class EmbeddingRequest:
    def __init__(self, text_segments: List[str]):
        self.text_segments = text_segments


class EmbeddingResponse:
    def __init__(self, embeddings: List[List[float]]):
        self.embeddings = embeddings


def embed_segments_for_translation_memory(
    request: EmbeddingRequest,
) -> EmbeddingResponse:
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

    embeddings = []
    for segment in request.text_segments:
        response = genai.embed_content(model="models/embedding-001", content=segment)
        embeddings.append(response["embedding"])

    return EmbeddingResponse(embeddings)
