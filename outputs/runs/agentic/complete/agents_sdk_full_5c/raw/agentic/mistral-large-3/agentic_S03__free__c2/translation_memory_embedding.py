from typing import List
import numpy as np
from sentence_transformers import SentenceTransformer

class TranslationMemoryEmbedder:
    def __init__(self):
        self.model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

    def embed_segments(self, segments: List[str]) -> List[List[float]]:
        embeddings = self.model.encode(segments, convert_to_tensor=False)
        return embeddings.tolist()