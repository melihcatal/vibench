# [LATER-STEP] translation_memory_embedding.py
"""Embed translated segments for translation-memory (TM) search.
Provides utilities to compute embeddings for source/target pairs and store them
in a searchable vector store (e.g., a simple in‑memory dict or an external service)."

from __future__ import annotations
import os
from typing import List, Dict, Any
import json
import hashlib
import numpy as np

# ---------------------------------------------------------------------------
# Placeholder for embedding model (e.g., OpenAI embeddings, sentence‑transformers)
# ---------------------------------------------------------------------------
try:
    import openai
except ImportError:
    openai = None

# ---------------------------------------------------------------------------
# Configuration (environment variables)
# ---------------------------------------------------------------------------
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if OPENAI_API_KEY:
    openai.api_key = OPENAI_API_KEY
else:
    print("Warning: OPENAI_API_KEY not set – embedding functions will raise.", file=sys.stderr)

# ---------------------------------------------------------------------------
# Embedding helper
# ---------------------------------------------------------------------------

def _embed_text(text: str) -> np.ndarray:
    """Return a numpy vector for the supplied text using OpenAI's embedding API.
    Adjust this function to swap out the provider/model as needed."
    """
    if not openai:
        raise RuntimeError("OpenAI SDK not installed. Please install the 'openai' package.")
    response = openai.Embedding.create(
        model="text-embedding-ada-002",
        input=text,
    )
    return np.array(response.data[0].embedding, dtype=np.float32)

# ---------------------------------------------------------------------------
# Data model for a TM entry
# ---------------------------------------------------------------------------

class TMEntry:
    """Simple container for a translation‑memory record.
    Stores source, target, and embeddings for fast similarity search."
    """
    def __init__(self, source: str, target: str):
        self.source = source
        self.target = target
        self.source_emb = None
        self.target_emb = None

    def compute_embeddings(self) -> None:
        """Calculate embeddings once upon first use."
        """
        if self.source_emb is None:
            self.source_emb = _embed_text(self.source)
        if self.target_emb is None:
            self.target_emb = _embed_text(self.target)

    def to_dict(self) -> Dict[str, Any]:
        self.compute_embeddings()
        return {
            "source": self.source,
            "target": self.target,
            "source_emb": self.source_emb.tolist(),
            "target_emb": self.target_emb.tolist(),
        }

# ---------------------------------------------------------------------------
# TM Store – simple in‑memory store (replace with vector DB for production)
# ---------------------------------------------------------------------------
class TranslationMemory:
    """In‑memory translation‑memory with nearest‑neighbor lookup based on embeddings."
    """
    def __init__(self):
        self.entries: List[TMEntry] = []

    def add(self, source: str, target: str) -> None:
        """Add a new translation pair to the memory.
        Embeddings are lazily computed when needed."
        """
        entry = TMEntry(source, target)
        entry.compute_embeddings()
        self.entries.append(entry)

    def find_most_similar(self, query: str, k: int = 5) -> List[Tuple[int, Dict[str, Any]]]:
        """Return the k most similar source segments to the query text.
        Returns list of (distance, entry_dict) tuples."
        """
        query_emb = _embed_text(query)
        scores = []
        for entry in self.entries:
            entry.compute_embeddings()  # ensure cached
            # Cosine similarity as dot product for normalized embeddings
            sim = np.dot(query_emb, entry.source_emb)  # embeddings are L2‑normalized by OpenAI
            scores.append((-sim, entry.to_dict()))  # negate for max‑heap behavior
        scores.sort()  # smallest (most similar) first
        return scores[:k]

# ---------------------------------------------------------------------------
# CLI entry point (optional, for quick testing)
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import argparse, json, sys
    parser = argparse.ArgumentParser(description="Add translations to TM and retrieve nearest matches.")
    parser.add_argument("--add", nargs=2, metavar=("SOURCE","TARGET"), help="Add a source/target pair to TM.")
    parser.add_argument("--search", type=str, help="Query source string to find similar translations.")
    parser.add_argument("--top_k", type=int, default=5, help="Number of nearest neighbors to return.")
    args = parser.parse_args()
    tm = TranslationMemory()
    if args.add:
        src, tgt = args.add
        tm.add(src, tgt)
        print(f"Added TM entry: {src} → {tgt}")
    if args.search:
        results = tm.find_most_similar(args.search, k=args.top_k)
        print(json.dumps([r[1] for r in results], indent=2))