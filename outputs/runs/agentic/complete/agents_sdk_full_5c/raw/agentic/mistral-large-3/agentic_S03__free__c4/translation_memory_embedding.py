from typing import List
import numpy as np
from sentence_transformers import SentenceTransformer

class TranslationMemoryEmbedder:
    def __init__(self):
        self.model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')  # Hugging Face model

    def embed_translations(self, source_texts: List[str], translated_texts: List[str]) -> np.ndarray:
        combined_texts = [
            f"Source: {source} | Translation: {translation}"
            for source, translation in zip(source_texts, translated_texts)
        ]
        
        embeddings = self.model.encode(combined_texts, convert_to_numpy=True)
        return embeddings