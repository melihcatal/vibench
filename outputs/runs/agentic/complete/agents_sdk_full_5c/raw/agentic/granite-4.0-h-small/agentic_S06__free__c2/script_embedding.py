# [LATER-STEP] script_embedding.py

from typing import List
from sentence_transformers import SentenceTransformer

def embed_script(script: str, model_name: str = "all-MiniLM-L6-v2") -> List[float]:
    """Embed a narration script using a pre-trained SentenceTransformer model.

    Args:
        script: Narration text.
        model_name: Hugging Face model identifier (default MiniLM).

    Returns:
        List of floats representing the embedding vector.
    """
    model = SentenceTransformer(model_name)
    return model.encode(script, convert_to_numpy=True).tolist()
