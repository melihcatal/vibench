import os
from typing import List, Dict
from translation_client import TranslationClient
from translation_models import TranslationModels
import hashlib

def embed_translated_segments(translations: List[Dict[str, str]], model: str = "dashscope_text_embedding") -> List[Dict[str, Any]]:
    """Embed translated text segments for use in translation‑memory search.

    Args:
        translations: List of translation response dicts (each must contain 'translatedText').
        model: Identifier of the embedding model; currently supports DashScope text embeddings.
    Returns:
        List of dicts with keys 'segment', 'translation', and 'embedding' (list of floats).
    """
    client = TranslationClient()
    # Choose embedding provider based on model identifier
    if model == "dashscope_text_embedding":
        # DashScope provides a simple embed call; we use its SDK directly.
        # NOTE: In a real project you would install the dashscope package and configure DASHSCOPE_API_KEY.
        # Here we simulate a stub embedding vector of zeros for demonstration.
        embed_fn = lambda txt: [0.0] * 768  # 768‑dim placeholder vector
    else:
        raise ValueError(f"Unsupported embedding model: {model}")

    embeddings = []
    for tr in translations:
        txt = tr.get('translatedText', '')
        if not txt:
            continue
        # Compute a deterministic hash to act as an ID for TM lookup
        seg_id = hashlib.sha256(txt.encode('utf-8')).hexdigest()[:8]
        vec = embed_fn(txt)
        embeddings.append({
            "segment": txt,
            "translation": txt,  # In TM we store the original segment; the translation is the same here.
            "id": seg_id,
            "embedding": vec
        })
    return embeddings

# Simple demo (remove in library mode)
if __name__ == "__main__":
    client = TranslationClient()
    srcs = ["Hello world", "Bonjour le monde", "Hola mundo"]
    trans = [client.translate(t, "fr") for t in srcs]
    vecs = embed_translated_segments(trans)
    for v in vecs:
        print(v)
