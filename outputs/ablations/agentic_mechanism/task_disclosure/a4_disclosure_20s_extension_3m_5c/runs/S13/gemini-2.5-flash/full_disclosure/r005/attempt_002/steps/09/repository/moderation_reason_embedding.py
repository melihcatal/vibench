import os
from typing import List

import vertexai
from vertexai.language_models import TextEmbeddingModel

def embed_rationales(rationales: List[str]) -> List[List[float]]:
    """Embeds moderation rationales for case retrieval using Vertex AI."""

    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    vertexai.init(project=project_id, location="us-central1")
    model = TextEmbeddingModel.from_pretrained("textembedding-gecko@003")
    embeddings = model.get_embeddings(rationales)
    return [embedding.values for embedding in embeddings]

