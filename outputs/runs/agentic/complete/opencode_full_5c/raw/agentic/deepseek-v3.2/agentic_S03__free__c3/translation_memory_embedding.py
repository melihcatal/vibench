import os
from typing import List, Dict, Any
import numpy as np
from sentence_transformers import SentenceTransformer


def embed_translated_segments(
    source_segments: List[str], translated_segments: List[str], language_pair: str
) -> Dict[str, Any]:
    """
    Embed translated segments for translation-memory search using SentenceTransformers.

    Args:
        source_segments: List of source text segments
        translated_segments: List of translated text segments
        language_pair: Language pair identifier (e.g., 'en-es')

    Returns:
        Dictionary with embeddings and metadata
    """
    # Load a multilingual embedding model from Hugging Face
    model = SentenceTransformer(
        "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    )

    # Combine source and translations for context-aware embedding
    combined_texts = []
    for src, trans in zip(source_segments, translated_segments):
        combined_texts.append(f"{language_pair}: {src} || {trans}")

    # Generate embeddings
    embeddings = model.encode(combined_texts, convert_to_numpy=True)

    # Also generate separate embeddings for source and translation
    source_embeddings = model.encode(source_segments, convert_to_numpy=True)
    translation_embeddings = model.encode(translated_segments, convert_to_numpy=True)

    return {
        "combined_embeddings": embeddings.tolist(),
        "source_embeddings": source_embeddings.tolist(),
        "translation_embeddings": translation_embeddings.tolist(),
        "language_pair": language_pair,
        "model": "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
        "embedding_dimension": embeddings.shape[1],
        "segment_count": len(source_segments),
    }


def find_similar_translations(
    query_text: str, translation_memory: Dict[str, Any], top_k: int = 5
) -> List[Dict[str, Any]]:
    """
    Find similar translations in memory using cosine similarity.

    Args:
        query_text: Text to find similar translations for
        translation_memory: Dictionary containing embeddings from embed_translated_segments
        top_k: Number of similar results to return

    Returns:
        List of similar translations with similarity scores
    """
    model = SentenceTransformer(
        "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    )

    # Embed query
    query_embedding = model.encode([query_text], convert_to_numpy=True)[0]

    # Get embeddings from memory
    memory_embeddings = np.array(translation_memory["combined_embeddings"])
    source_texts = translation_memory.get("source_texts", [])
    translation_texts = translation_memory.get("translation_texts", [])

    # Calculate cosine similarities
    similarities = np.dot(memory_embeddings, query_embedding) / (
        np.linalg.norm(memory_embeddings, axis=1) * np.linalg.norm(query_embedding)
    )

    # Get top-k similar items
    top_indices = np.argsort(similarities)[-top_k:][::-1]

    results = []
    for idx in top_indices:
        results.append(
            {
                "source_text": source_texts[idx]
                if idx < len(source_texts)
                else f"Segment {idx}",
                "translation": translation_texts[idx]
                if idx < len(translation_texts)
                else f"Translation {idx}",
                "similarity_score": float(similarities[idx]),
                "index": int(idx),
            }
        )

    return results
