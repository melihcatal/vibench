from typing import List
import numpy as np
from sentence_transformers import SentenceTransformer
from translation_models import TranslationMemoryRequest, TranslationMemoryResponse

class TranslationMemoryEmbedder:
    def __init__(self):
        self.model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

    def embed_segments(self, segments: List[str]) -> List[List[float]]:
        return self.model.encode(segments, convert_to_numpy=True).tolist()

def embed_translation_memory(request: TranslationMemoryRequest) -> TranslationMemoryResponse:
    embedder = TranslationMemoryEmbedder()
    embeddings = embedder.embed_segments(request.segments)
    return TranslationMemoryResponse(
        embeddings=embeddings,
        model_used="paraphrase-multilingual-MiniLM-L12-v2"
    )