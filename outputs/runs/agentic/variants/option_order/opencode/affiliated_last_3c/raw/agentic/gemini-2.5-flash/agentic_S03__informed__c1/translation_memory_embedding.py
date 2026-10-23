import google.generativeai as genai
import os
from translation_models import TranslationMemoryEmbeddingRequest
from typing import List

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def embed_segment_for_translation_memory(
    request: TranslationMemoryEmbeddingRequest,
) -> List[float]:
    model = "models/embedding-001"
    response = genai.embed_content(model=model, content=request.segment)
    return response["embedding"]
