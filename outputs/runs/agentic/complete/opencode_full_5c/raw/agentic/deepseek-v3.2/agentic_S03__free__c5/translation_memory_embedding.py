import os
import numpy as np
from typing import List, Dict, Any, Tuple
from translation_models import TranslationResponse


def embed_translated_segments(
    original_text: str,
    translated_text: str,
    source_lang: str = "en",
    target_lang: str = "es",
) -> Dict[str, Any]:
    """
    Embed translated segments for translation-memory search using Google Cloud Vertex AI.

    Args:
        original_text: Original source text
        translated_text: Translated text
        source_lang: Source language code
        target_lang: Target language code

    Returns:
        Dictionary with embeddings and metadata
    """
    try:
        # Import Google Cloud Vertex AI for embeddings
        from google.cloud import aiplatform
        import vertexai
        from vertexai.language_models import TextEmbeddingModel

        # Initialize Vertex AI
        project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
        location = os.environ.get("GOOGLE_CLOUD_REGION", "us-central1")

        if not project_id:
            raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set")

        # Initialize Vertex AI
        vertexai.init(project=project_id, location=location)

        # Load the text embedding model
        model = TextEmbeddingModel.from_pretrained("textembedding-gecko@001")

        # Generate embeddings for original text
        original_embeddings = model.get_embeddings([original_text])
        original_embedding = original_embeddings[0].values

        # Generate embeddings for translated text
        translated_embeddings = model.get_embeddings([translated_text])
        translated_embedding = translated_embeddings[0].values

        # Calculate cosine similarity between embeddings
        similarity = cosine_similarity(original_embedding, translated_embedding)

        # Create segment metadata
        segment_metadata = {
            "original_text": original_text,
            "translated_text": translated_text,
            "source_lang": source_lang,
            "target_lang": target_lang,
            "original_length": len(original_text),
            "translated_length": len(translated_text),
            "embedding_dimension": len(original_embedding),
            "similarity_score": float(similarity),
            "model_used": "textembedding-gecko@001",
            "timestamp": get_current_timestamp(),
        }

        # Prepare embedding storage format
        embedding_data = {
            "metadata": segment_metadata,
            "embeddings": {
                "original": original_embedding,
                "translated": translated_embedding,
            },
            "vector_db_ready": True,
        }

        return embedding_data

    except Exception as e:
        raise Exception(f"Embedding generation failed: {str(e)}")


def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """
    Calculate cosine similarity between two vectors.

    Args:
        vec1: First vector
        vec2: Second vector

    Returns:
        Cosine similarity score
    """
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)

    dot_product = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)

    if norm1 == 0 or norm2 == 0:
        return 0.0

    return dot_product / (norm1 * norm2)


def search_translation_memory(
    query_text: str, language_code: str = "en", top_k: int = 5
) -> List[Dict[str, Any]]:
    """
    Search translation memory using embeddings.

    Args:
        query_text: Text to search for
        language_code: Language code of query text
        top_k: Number of results to return

    Returns:
        List of similar translation pairs
    """
    try:
        # This is a placeholder for actual vector database search
        # In production, this would connect to a vector DB like Pinecone, Weaviate, or Vertex AI Matching Engine

        from google.cloud import aiplatform
        import vertexai
        from vertexai.language_models import TextEmbeddingModel

        project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
        location = os.environ.get("GOOGLE_CLOUD_REGION", "us-central1")

        if not project_id:
            raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set")

        vertexai.init(project=project_id, location=location)
        model = TextEmbeddingModel.from_pretrained("textembedding-gecko@001")

        # Generate query embedding
        query_embeddings = model.get_embeddings([query_text])
        query_embedding = query_embeddings[0].values

        # In a real implementation, this would query a vector database
        # For now, return mock results
        mock_results = [
            {
                "original_text": "Hello world",
                "translated_text": "Hola mundo",
                "source_lang": "en",
                "target_lang": "es",
                "similarity": 0.85,
                "confidence": "HIGH",
            },
            {
                "original_text": "Good morning",
                "translated_text": "Buenos días",
                "source_lang": "en",
                "target_lang": "es",
                "similarity": 0.78,
                "confidence": "MEDIUM",
            },
        ]

        return mock_results[:top_k]

    except Exception as e:
        raise Exception(f"Translation memory search failed: {str(e)}")


def get_current_timestamp() -> str:
    """Get current timestamp in ISO format."""
    from datetime import datetime

    return datetime.utcnow().isoformat() + "Z"
