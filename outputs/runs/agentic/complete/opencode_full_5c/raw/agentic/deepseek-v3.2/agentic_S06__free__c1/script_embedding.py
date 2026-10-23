import os
import numpy as np
from google.cloud import aiplatform


def embed_narration_script(text, project_id=None, location="us-central1"):
    """Embed narration scripts for voice-asset search using Google Vertex AI Text Embeddings."""

    if project_id is None:
        project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
        if not project_id:
            raise ValueError("Google Cloud project ID must be provided")

    aiplatform.init(project=project_id, location=location)

    from google.cloud.aiplatform import TextEmbeddingModel

    model = TextEmbeddingModel.from_pretrained("textembedding-gecko@001")

    embeddings = model.get_embeddings([text])

    embedding_vector = embeddings[0].values

    return {
        "embedding": np.array(embedding_vector),
        "dimensions": len(embedding_vector),
        "model": "textembedding-gecko@001",
        "text_length": len(text),
    }


def embed_batch_for_search(texts, project_id=None):
    """Embed multiple narration scripts for search indexing."""
    if project_id is None:
        project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
        if not project_id:
            raise ValueError("Google Cloud project ID must be provided")

    aiplatform.init(project=project_id, location="us-central1")

    from google.cloud.aiplatform import TextEmbeddingModel

    model = TextEmbeddingModel.from_pretrained("textembedding-gecko@001")

    embeddings = model.get_embeddings(texts)

    results = []
    for i, emb in enumerate(embeddings):
        results.append(
            {
                "text": texts[i],
                "embedding": np.array(emb.values),
                "dimensions": len(emb.values),
            }
        )

    return results
