# translation_memory_embedding.py
from typing import List
from translation_models import TranslateResponse
import numpy as np


def embed_translation(translation: TranslateResponse) -> np.ndarray:
    """Create a simple embedding vector for a translated segment."""
    # Placeholder: in real usage replace with model like sentence-transformers
    text = translation["translated_text"]
    # Hash based dummy embedding (32-length vector)
    return np.array([hash(c) % 256 for c in text])[:32]


def build_embedding_index(
    translations: List[TranslateResponse],
) -> dict[str, np.ndarray]:
    """Map original text to its embedding for TM search."""
    index = {}
    for i, trans in enumerate(translations):
        key = f"TM_{i}"  # unique key for memory
        index[key] = embed_translation(trans)
    return index
