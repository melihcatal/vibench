# [LATER-STEP] script_embedding.py

from typing import List, Tuple
import numpy as np
from sentence_transformers import SentenceTransformer

# Load a lightweight multilingual model (e.g., "paraphrase-multilingual-MiniLM-L12-v2")
model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")


def embed_script(text: str) -> np.ndarray:
    """Embeds a narration script into a vector space.

    Args:
        text: Full script text.

    Returns:
        Mean embedding vector (float32 ndarray) representing the script.
    """
    embeddings = model.encode(text, convert_to_tensor=True)
    return np.mean(embeddings, axis=0) if embeddings.ndim > 1 else embeddings


def find_closest_voice(
    embedded_script: np.ndarray, voice_embeddings: List[Tuple[str, np.ndarray]]
) -> str:
    """
    Finds the voice whose embedding is most similar (cosine similarity) to the script.

    Args:
        embedded_script: Pre‑computed script vector.
        voice_embeddings: List of (voice_name, vector) pairs.

    Returns:
        Voice name with highest similarity.
    """
    best_name, _ = max(
        voice_embeddings,
        key=lambda pair: (
            np.dot(embedded_script, pair[1])
            / (np.linalg.norm(embedded_script) * np.linalg.norm(pair[1]))
        ),
    )
    return best_name


# Example usage (requires voice embedding data):
# voices = [("en-US-Standard-A", np.random.rand(384)), ("en-US-Standard-B", np.random.rand(384))]
# script_vec = embed_script("Welcome to the demo.")
# selected = find_closest_voice(script_vec, voices)
# print(selected)
