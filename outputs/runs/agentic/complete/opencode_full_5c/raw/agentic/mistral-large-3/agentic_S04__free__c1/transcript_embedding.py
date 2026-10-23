from google.cloud import aiplatform
from typing import List, Dict
import numpy as np


def transcript_embedding(transcript_segments: List[str]) -> List[Dict[str, Any]]:
    """Embed transcript segments for semantic retrieval using Google Cloud Vertex AI."""
    aiplatform.init(project="your-project-id", location="us-central1")

    model = aiplatform.TextEmbeddingModel.from_pretrained("textembedding-gecko@latest")

    embeddings = model.get_embeddings(transcript_segments)

    return [
        {
            "segment": segment,
            "embedding": embedding.values,
            "dimensions": len(embedding.values),
        }
        for segment, embedding in zip(transcript_segments, embeddings)
    ]
