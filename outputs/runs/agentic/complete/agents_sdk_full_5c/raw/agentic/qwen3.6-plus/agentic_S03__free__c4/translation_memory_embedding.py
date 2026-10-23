"""
Embed translated segments for translation-memory search.
Uses OpenAI Embeddings API (text-embedding-ada-002) to create vector
embeddings of translated text segments for translation-memory similarity search.
Provider: OpenAI (api.openai.com)
Model: text-embedding-ada-002
"""

from typing import Optional, List, Dict, Any
import os
import hashlib
import json

import openai

from translation_models import TranslationResponse


OPENAI_EMBEDDING_MODEL = "text-embedding-ada-002"
OPENAI_API_BASE = "https://api.openai.com/v1"
OPENAI_API_KEY_ENV = "OPENAI_API_KEY"


def create_openai_client(
    api_key: Optional[str] = None,
) -> openai.OpenAI:
    """
    Create an OpenAI API client for embedding generation.
    
    Uses openai.OpenAI to connect to api.openai.com for embedding
    generation with the text-embedding-ada-002 model.
    
    Args:
        api_key: OpenAI API key. Falls back to OPENAI_API_KEY env var.
    
    Returns:
        Configured openai.OpenAI client instance.
    """
    if api_key:
        os.environ[OPENAI_API_KEY_ENV] = api_key
    
    client = openai.OpenAI(
        api_key=os.environ.get(OPENAI_API_KEY_ENV, ""),
        base_url=OPENAI_API_BASE,
    )
    
    return client


def generate_segment_id(text: str) -> str:
    """
    Generate a unique ID for a text segment.
    
    Args:
        text: Text segment to generate ID for.
    
    Returns:
        MD5 hash string of the text.
    """
    return hashlib.md5(text.encode("utf-8")).hexdigest()


def embed_translation_segment(
    text: str,
    client: openai.OpenAI,
    model: str = OPENAI_EMBEDDING_MODEL,
) -> Dict[str, Any]:
    """
    Generate embedding for a single translated text segment.
    
    Uses the openai client to call api.openai.com with the
    text-embedding-ada-002 model for vector generation.
    
    Args:
        text: Text segment to embed.
        client: OpenAI client instance.
        model: Embedding model identifier (default: text-embedding-ada-002).
    
    Returns:
        Dict with embedding vector, segment_id, and metadata.
    """
    if not text or not text.strip():
        return {
            "embedding": [],
            "segment_id": "",
            "model": model,
            "text_length": 0,
        }
    
    try:
        response = client.embeddings.create(
            input=text,
            model=model,
        )
        
        embedding = response.data[0].embedding
        
        return {
            "embedding": embedding,
            "segment_id": generate_segment_id(text),
            "model": model,
            "text_length": len(text),
            "token_count": response.usage.total_tokens if response.usage else 0,
        }
    
    except Exception as e:
        return {
            "embedding": [],
            "segment_id": "",
            "model": model,
            "text_length": len(text),
            "error": str(e),
        }


def embed_translation_memory(
    translation_response: TranslationResponse,
    api_key: Optional[str] = None,
    model: str = OPENAI_EMBEDDING_MODEL,
) -> Dict[str, Any]:
    """
    Embed all translated segments for translation-memory storage and search.
    
    Uses OpenAI's text-embedding-ada-002 model via api.openai.com to generate
    vector embeddings for each translated segment. These embeddings can be
    stored and used for similarity-based translation-memory lookup.
    
    Args:
        translation_response: TranslationResponse with segments to embed.
        api_key: OpenAI API key.
        model: Embedding model to use (default: text-embedding-ada-002).
    
    Returns:
        Dict with embedded segments, metadata, and search-ready index.
    """
    client = create_openai_client(api_key=api_key)
    
    if not translation_response.success or not translation_response.results:
        return {
            "segments": [],
            "index_size": 0,
            "model_used": model,
            "success": False,
            "error": "No translation results to embed",
        }
    
    embedded_segments = []
    total_tokens = 0
    
    for result in translation_response.results:
        combined_text = f"{result.original_text} ||| {result.translated_text}"
        
        embedding_result = embed_translation_segment(
            text=combined_text,
            client=client,
            model=model,
        )
        
        segment_entry = {
            "segment_id": embedding_result.get("segment_id", generate_segment_id(combined_text)),
            "source_text": result.original_text,
            "target_text": result.translated_text,
            "source_language": result.source_language,
            "target_language": result.target_language,
            "embedding": embedding_result.get("embedding", []),
            "model": model,
        }
        
        embedded_segments.append(segment_entry)
        total_tokens += embedding_result.get("token_count", 0)
    
    return {
        "segments": embedded_segments,
        "index_size": len(embedded_segments),
        "model_used": model,
        "total_tokens": total_tokens,
        "success": True,
    }


def compute_embedding_similarity(
    embedding_a: List[float],
    embedding_b: List[float],
) -> float:
    """
    Compute cosine similarity between two embedding vectors.
    
    Args:
        embedding_a: First embedding vector.
        embedding_b: Second embedding vector.
    
    Returns:
        Cosine similarity score between 0 and 1.
    """
    if not embedding_a or not embedding_b:
        return 0.0
    
    dot_product = sum(a * b for a, b in zip(embedding_a, embedding_b))
    magnitude_a = sum(a * a for a in embedding_a) ** 0.5
    magnitude_b = sum(b * b for b in embedding_b) ** 0.5
    
    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0
    
    return dot_product / (magnitude_a * magnitude_b)


def search_translation_memory(
    query_embedding: List[float],
    memory_index: Dict[str, Any],
    top_k: int = 5,
    threshold: float = 0.7,
) -> List[Dict[str, Any]]:
    """
    Search translation memory for similar segments using embedding similarity.
    
    Args:
        query_embedding: Embedding vector for the query segment.
        memory_index: Index dict from embed_translation_memory.
        top_k: Number of top results to return.
        threshold: Minimum similarity threshold.
    
    Returns:
        List of matching segments sorted by similarity.
    """
    results = []
    
    for segment in memory_index.get("segments", []):
        similarity = compute_embedding_similarity(
            query_embedding,
            segment.get("embedding", []),
        )
        
        if similarity >= threshold:
            results.append({
                "segment": segment,
                "similarity": round(similarity, 4),
            })
    
    results.sort(key=lambda x: x["similarity"], reverse=True)
    
    return results[:top_k]


def serialize_translation_memory(
    memory_index: Dict[str, Any],
    filepath: str,
) -> None:
    """
    Serialize translation memory index to JSON file.
    
    Args:
        memory_index: Index dict from embed_translation_memory.
        filepath: Path to save the JSON file.
    """
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(memory_index, f, indent=2)


def load_translation_memory(
    filepath: str,
) -> Dict[str, Any]:
    """
    Load translation memory index from JSON file.
    
    Args:
        filepath: Path to the JSON file.
    
    Returns:
        Loaded translation memory index.
    """
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


if __name__ == "__main__":
    from translate_text import translate_text
    
    response = translate_text("Welcome to our service", target_language="fr")
    if response.success:
        memory = embed_translation_memory(response)
        print(f"Embedded {memory['index_size']} segments")
        print(f"Model used: {memory['model_used']}")
