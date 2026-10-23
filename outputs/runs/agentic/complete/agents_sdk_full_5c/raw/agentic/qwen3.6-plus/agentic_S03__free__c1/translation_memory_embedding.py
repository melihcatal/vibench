"""Embed translated segments for translation-memory search using OpenAI embeddings API."""

import os
import json
import hashlib
from typing import List, Dict, Any, Optional, Tuple
import numpy as np
from openai import OpenAI
from translation_client import load_translation_config
from translation_models import count_tokens_approx


OPENAI_EMBEDDING_MODEL = "text-embedding-ada-002"
OPENAI_EMBEDDING_DIMENSIONS = 1536


class TranslationMemoryEntry:
    """Represents a single entry in the translation memory."""

    def __init__(
        self,
        source_text: str,
        translated_text: str,
        source_lang: str,
        target_lang: str,
        source_embedding: Optional[List[float]] = None,
        translated_embedding: Optional[List[float]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        self.source_text = source_text
        self.translated_text = translated_text
        self.source_lang = source_lang
        self.target_lang = target_lang
        self.source_embedding = source_embedding or []
        self.translated_embedding = translated_embedding or []
        self.metadata = metadata or {}
        self.entry_id = self._generate_id()

    def _generate_id(self) -> str:
        """Generate a unique ID for this entry."""
        content = f"{self.source_text}|{self.translated_text}|{self.source_lang}|{self.target_lang}"
        return hashlib.md5(content.encode("utf-8")).hexdigest()[:12]

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "entry_id": self.entry_id,
            "source_text": self.source_text,
            "translated_text": self.translated_text,
            "source_lang": self.source_lang,
            "target_lang": self.target_lang,
            "source_embedding": self.source_embedding,
            "translated_embedding": self.translated_embedding,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TranslationMemoryEntry":
        """Create entry from dictionary."""
        return cls(
            source_text=data["source_text"],
            translated_text=data["translated_text"],
            source_lang=data["source_lang"],
            target_lang=data["target_lang"],
            source_embedding=data.get("source_embedding", []),
            translated_embedding=data.get("translated_embedding", []),
            metadata=data.get("metadata", {}),
        )


def embed_text(text: str, model: str = OPENAI_EMBEDDING_MODEL) -> List[float]:
    """Generate embedding for a text segment using OpenAI API.

    Args:
        text: Text to embed.
        model: OpenAI embedding model identifier.

    Returns:
        List of floats representing the embedding vector.
    """
    config = load_translation_config()
    api_key = os.environ.get("OPENAI_API_KEY", config.get("openai_api_key"))

    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable or config is required")

    client = OpenAI(api_key=api_key)

    response = client.embeddings.create(
        model=model,
        input=text,
    )

    return response.data[0].embedding


def embed_translation_pair(
    source_text: str,
    translated_text: str,
) -> Tuple[List[float], List[float]]:
    """Embed both source and translated text for translation memory.

    Args:
        source_text: Source language text.
        translated_text: Target language text.

    Returns:
        Tuple of (source_embedding, translated_embedding).
    """
    source_embedding = embed_text(source_text)
    translated_embedding = embed_text(translated_text)
    return source_embedding, translated_embedding


def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """Calculate cosine similarity between two vectors.

    Args:
        vec1: First vector.
        vec2: Second vector.

    Returns:
        Cosine similarity score between -1 and 1.
    """
    v1 = np.array(vec1)
    v2 = np.array(vec2)

    norm1 = np.linalg.norm(v1)
    norm2 = np.linalg.norm(v2)

    if norm1 == 0 or norm2 == 0:
        return 0.0

    return float(np.dot(v1, v2) / (norm1 * norm2))


class TranslationMemoryIndex:
    """Index for storing and searching translation memory entries."""

    def __init__(self):
        self.entries: List[TranslationMemoryEntry] = []
        self._index_built = False

    def add_entry(self, entry: TranslationMemoryEntry) -> None:
        """Add a translation memory entry to the index."""
        self.entries.append(entry)
        self._index_built = False

    def add_entries(self, entries: List[TranslationMemoryEntry]) -> None:
        """Add multiple entries to the index."""
        self.entries.extend(entries)
        self._index_built = False

    def build_index(self, source_lang: str = "en") -> None:
        """Ensure all entries have embeddings."""
        for entry in self.entries:
            if not entry.source_embedding:
                entry.source_embedding = embed_text(entry.source_text)
            if not entry.translated_embedding:
                entry.translated_embedding = embed_text(entry.translated_text)
        self._index_built = True

    def search(
        self,
        query_text: str,
        top_k: int = 5,
        similarity_threshold: float = 0.7,
    ) -> List[Dict[str, Any]]:
        """Search translation memory for similar segments.

        Args:
            query_text: Text to search for.
            top_k: Number of results to return.
            similarity_threshold: Minimum similarity score.

        Returns:
            List of matching entries with similarity scores.
        """
        if not self._index_built:
            self.build_index()

        query_embedding = embed_text(query_text)

        results = []
        for entry in self.entries:
            if not entry.source_embedding:
                continue

            similarity = cosine_similarity(query_embedding, entry.source_embedding)

            if similarity >= similarity_threshold:
                results.append({
                    "entry": entry.to_dict(),
                    "similarity_score": round(similarity, 4),
                })

        results.sort(key=lambda x: x["similarity_score"], reverse=True)
        return results[:top_k]

    def to_dict(self) -> Dict[str, Any]:
        """Serialize the entire index."""
        return {
            "entries": [entry.to_dict() for entry in self.entries],
            "entry_count": len(self.entries),
        }

    def save(self, filepath: str) -> None:
        """Save index to JSON file."""
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, ensure_ascii=False, indent=2)

    @classmethod
    def load(cls, filepath: str) -> "TranslationMemoryIndex":
        """Load index from JSON file."""
        index = cls()
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        for entry_data in data.get("entries", []):
            index.entries.append(TranslationMemoryEntry.from_dict(entry_data))
        return index


if __name__ == "__main__":
    import sys

    index = TranslationMemoryIndex()

    sample_pairs = [
        ("Hello, how are you?", "Bonjour, comment allez-vous?", "en", "fr"),
        ("Thank you very much.", "Merci beaucoup.", "en", "fr"),
        ("Good morning!", "Bonjour!", "en", "fr"),
    ]

    for src, tgt, src_lang, tgt_lang in sample_pairs:
        src_emb, tgt_emb = embed_translation_pair(src, tgt)
        entry = TranslationMemoryEntry(src, tgt, src_lang, tgt_lang, src_emb, tgt_emb)
        index.add_entry(entry)

    if len(sys.argv) > 1:
        query = sys.argv[1]
        results = index.search(query, top_k=3)
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        print("Usage: translation_memory_embedding.py <query_text>")
