# translation_memory_embedding.py – Embed translated segments for TM search
import json
from typing import List, Dict
import numpy as np

from translation_client import GeneralTextTranslationClient
from translation_models import _normalize_response

# Assume an embedding SDK is installed, e.g., openai, google-genai, etc.
# from openai import Embedding

EMBED_TYPE = "text-embedding-3-large"  # example for OpenAI


def embed_translations(
    translations: List[Dict[str, Any]], model: str = EMBED_TYPE
) -> List[Dict[str, Any]]:
    """Generate embeddings for translated texts to enable similarity search in a TM.",
    Args:
        translations (List[Dict[str, Any]]): Normalized translation responses.
        model (str): Embedding model identifier.
    Returns:
        List[Dict[str, Any]]: Each dict includes the original translated text and its embedding vector.
    """
    # Extract only the translated text strings
    texts = [t["translated_text"] for t in translations if "translated_text" in t]
    # ---- Placeholder embedding call ----
    # embeddings = Embedding.create(model=model, input=texts)["data"]
    # For demo we create dummy vectors
    # ---- End placeholder ----
    dummy_embeddings = [
        np.random.rand(1536).tolist() for _ in texts
    ]  # 1536-dim vector example
    embedded = []
    for i, trans in enumerate(translations):
        if "translated_text" in trans:
            embedded.append(
                {
                    "translated_text": trans["translated_text"],
                    "embedding": dummy_embeddings[i],
                }
            )
    return embedded


# Demo (requires real embedding SDK to be functional)
# client = GeneralTextTranslationClient()
# raw = client.translate(texts=["Hello", "World"], source_lang="en", target_lang="zh")
# norm = [_normalize_response(r) for r in raw]
# embeddings = embed_translations(norm)
# print(embeddings)
