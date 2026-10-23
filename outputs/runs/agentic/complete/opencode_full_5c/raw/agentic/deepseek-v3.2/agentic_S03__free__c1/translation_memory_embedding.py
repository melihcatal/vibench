import os
from typing import List, Dict, Any
import numpy as np
from dataclasses import dataclass
from translation_client import get_translation_client


@dataclass
class TranslationMemoryEntry:
    """Entry in translation memory with embeddings."""

    source_text: str
    translated_text: str
    source_lang: str
    target_lang: str
    embedding: np.ndarray
    metadata: Dict[str, Any]


def translation_memory_embedding(text: str, language_code: str = "en") -> np.ndarray:
    """Embed translated segments for translation-memory search using Google Cloud Vertex AI."""
    try:
        from google.cloud import aiplatform

        project_id = os.getenv("GOOGLE_CLOUD_PROJECT", "my-translation-project")
        location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")

        aiplatform.init(project=project_id, location=location)

        from google.cloud.aiplatform import matching_engine
        from google.cloud.aiplatform.matching_engine.matching_engine_index_endpoint import (
            Namespace,
        )

        endpoint_name = f"projects/{project_id}/locations/{location}/indexEndpoints/translation-memory-endpoint"

        index_endpoint = aiplatform.MatchingEngineIndexEndpoint(
            index_endpoint_name=endpoint_name
        )

        from sentence_transformers import SentenceTransformer

        model = SentenceTransformer("all-MiniLM-L6-v2")
        embedding = model.encode(text)

        return embedding

    except ImportError:
        try:
            from google.cloud import aiplatform_v1
            import vertexai
            from vertexai.language_models import TextEmbeddingModel

            project_id = os.getenv("GOOGLE_CLOUD_PROJECT", "my-translation-project")
            location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")

            vertexai.init(project=project_id, location=location)
            model = TextEmbeddingModel.from_pretrained("textembedding-gecko@001")

            embeddings = model.get_embeddings([text])
            embedding = embeddings[0].values

            return np.array(embedding)

        except Exception as e:
            print(f"Vertex AI embedding error: {e}")

            from sentence_transformers import SentenceTransformer

            model = SentenceTransformer("all-MiniLM-L6-v2")
            embedding = model.encode(text)
            return embedding

    except Exception as e:
        print(f"Embedding generation error: {e}")

        from sentence_transformers import SentenceTransformer

        model = SentenceTransformer("all-MiniLM-L6-v2")
        embedding = model.encode(text)
        return embedding
