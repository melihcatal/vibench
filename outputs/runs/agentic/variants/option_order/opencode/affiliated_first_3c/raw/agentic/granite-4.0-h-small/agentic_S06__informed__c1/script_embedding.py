import os
import json
import requests
import hashlib


def embed_script(script_text: str) -> dict:
    """Generate an embedding vector for a narration script using OpenAI embeddings."""
    EMBED_API = os.getenv("OPENAI_API_KEY")
    if not EMBED_API:
        raise RuntimeError("Set OPENAI_API_KEY environment variable for embedding")
    url = "https://api.openai.com/v1/embeddings"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {EMBED_API}",
    }
    payload = {"model": "text-embedding-ada-002", "input": script_text}
    resp = requests.post(url, headers=headers, json=payload)
    resp.raise_for_status()
    data = resp.json()
    vec = data["data"][0]["embedding"]
    # Store a hash of the script for later lookup
    script_hash = hashlib.sha256(script_text.encode("utf-8")).hexdigest()
    return {"hash": script_hash, "embedding": vec}


class ScriptEmbedding:
    """Helper to compute and query embeddings for voice‑asset search."""

    @staticmethod
    def create_or_update(script_text: str) -> dict:
        """Return existing entry if hash matches, otherwise store new embedding."""
        # Placeholder: in real pipeline you'd write the JSON to a vector store database
        return embed_script(script_text)

    @staticmethod
    def find_closest(hash_val: str, search_texts: list) -> list:
        """Dummy method – replace with your nearest‑neighbor query logic."""
        return [{"text": txt, "distance": 0.1} for txt in search_texts]
