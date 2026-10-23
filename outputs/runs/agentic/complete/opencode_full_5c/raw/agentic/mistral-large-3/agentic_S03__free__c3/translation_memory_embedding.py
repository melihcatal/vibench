from typing import List, Dict
from sentence_transformers import SentenceTransformer
import numpy as np


class TranslationMemoryEmbedder:
    def __init__(self):
        self.model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

    def embed_segments(self, segments: List[str]) -> List[List[float]]:
        return self.model.encode(segments, convert_to_numpy=True).tolist()


def embed_translated_segments(segments: List[Dict[str, str]]) -> Dict[str, List[float]]:
    embedder = TranslationMemoryEmbedder()
    texts = [segment["translated_text"] for segment in segments]
    embeddings = embedder.embed_segments(texts)

    return {
        segment["id"]: embedding for segment, embedding in zip(segments, embeddings)
    }
