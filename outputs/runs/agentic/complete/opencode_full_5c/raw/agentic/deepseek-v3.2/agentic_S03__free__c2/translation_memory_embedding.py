import os
from typing import List, Dict, Any, Tuple
import numpy as np
from translation_client import TranslationClient


def translation_memory_embedding(
    segment_pairs: List[Tuple[str, str]],
    source_lang: str = "en",
    target_lang: str = "es",
) -> Dict[str, Any]:
    """
    Embed translated segments for translation-memory search using Google Cloud Vertex AI.

    Args:
        segment_pairs: List of (source_text, translated_text) tuples
        source_lang: Source language code
        target_lang: Target language code

    Returns:
        Dictionary with embeddings and search index
    """
    client = TranslationClient()

    # Use Google Cloud Vertex AI for embeddings
    try:
        from google.cloud import aiplatform

        # Initialize Vertex AI
        project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
        location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")

        if not project_id:
            raise ValueError("GOOGLE_CLOUD_PROJECT environment variable must be set")

        aiplatform.init(project=project_id, location=location)

        # Use text-embedding model
        from vertexai.language_models import TextEmbeddingModel

        model = TextEmbeddingModel.from_pretrained("text-embedding-004")

        # Prepare texts for embedding
        all_texts = []
        for source, target in segment_pairs:
            all_texts.append(f"Source ({source_lang}): {source}")
            all_texts.append(f"Target ({target_lang}): {target}")

        # Generate embeddings
        embeddings = model.get_embeddings(all_texts)

        # Extract embedding vectors
        embedding_vectors = []
        for emb in embeddings:
            embedding_vectors.append(emb.values)

        # Create search index structure
        index_data = []
        for i, (source, target) in enumerate(segment_pairs):
            source_emb = embedding_vectors[i * 2]
            target_emb = embedding_vectors[i * 2 + 1]

            index_data.append(
                {
                    "id": f"segment_{i}",
                    "source_text": source,
                    "target_text": target,
                    "source_embedding": source_emb,
                    "target_embedding": target_emb,
                    "source_lang": source_lang,
                    "target_lang": target_lang,
                }
            )

        # Calculate average embedding for quick similarity search
        all_embeddings = np.array(embedding_vectors)
        centroid = np.mean(all_embeddings, axis=0)

        return {
            "segment_count": len(segment_pairs),
            "embeddings_generated": len(embedding_vectors),
            "embedding_dimension": len(embedding_vectors[0])
            if embedding_vectors
            else 0,
            "search_index": index_data,
            "centroid_embedding": centroid.tolist(),
            "provider": "google-vertex-ai",
            "model_used": "text-embedding-004",
        }

    except ImportError:
        # Fallback to simpler embedding approach
        return simple_embedding_fallback(segment_pairs, source_lang, target_lang)
    except Exception as e:
        print(f"Vertex AI error: {e}")
        return simple_embedding_fallback(segment_pairs, source_lang, target_lang)


def simple_embedding_fallback(
    segment_pairs: List[Tuple[str, str]], source_lang: str, target_lang: str
) -> Dict[str, Any]:
    """Simple embedding fallback using basic text features."""

    # Create simple bag-of-words like embeddings
    index_data = []

    for i, (source, target) in enumerate(segment_pairs):
        # Simple feature extraction
        source_words = set(source.lower().split())
        target_words = set(target.lower().split())

        # Create simple embedding (word presence vector)
        all_words = list(source_words.union(target_words))

        # Simple one-hot like encoding
        source_vector = [1 if word in source_words else 0 for word in all_words]
        target_vector = [1 if word in target_words else 0 for word in all_words]

        index_data.append(
            {
                "id": f"segment_{i}",
                "source_text": source,
                "target_text": target,
                "source_embedding": source_vector,
                "target_embedding": target_vector,
                "source_lang": source_lang,
                "target_lang": target_lang,
                "vocabulary": all_words,
            }
        )

    return {
        "segment_count": len(segment_pairs),
        "embeddings_generated": len(index_data) * 2,
        "embedding_dimension": len(index_data[0]["source_embedding"])
        if index_data
        else 0,
        "search_index": index_data,
        "provider": "simple-bow-fallback",
        "model_used": "bag-of-words",
    }
