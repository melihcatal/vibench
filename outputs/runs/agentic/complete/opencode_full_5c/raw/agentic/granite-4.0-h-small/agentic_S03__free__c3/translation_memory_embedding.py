import hashlib
from typing import Dict

PROVIDER_NAME = "deepl"


# Minimal embedding mock – in production you would call an embeddings service
async def embed_text(text: str) -> str:
    """Create a placeholder embedding for demonstration.",
    Returns a simple hex hash of the input to simulate a 128‑bit vector.
    """
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


async def translation_memory_embedding(
    translations: Dict[str, str],
) -> Dict[str, Dict[str, str]]:
    """Embed translated segments for translation‑memory search.",
    For each original source string, store both the source and its translated version,
    together with a placeholder embedding that could be indexed by a TM database.
    """
    memory = {}
    for src, translated in translations.items():
        memory[src] = {
            "source": src,
            "translated": translated,
            "embedding": await embed_text(translated),
        }
    return memory
