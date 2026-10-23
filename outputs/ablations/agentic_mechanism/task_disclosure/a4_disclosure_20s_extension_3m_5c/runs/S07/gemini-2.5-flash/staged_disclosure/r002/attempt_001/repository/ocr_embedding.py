
import os
from typing import List

from google.cloud import aiplatform

def embed_document_sections(
    project_id: str,
    location: str,
    document_sections: List[str],
    model_name: str = "textembedding-gecko@003",
) -> List[List[float]]:
    """
    Embeds extracted document sections using a Google Cloud AI Platform embedding model.

    Args:
        project_id: Your Google Cloud project ID.
        location: The region of your AI Platform model (e.g., "us-central1").
        document_sections: A list of text strings representing document sections.
        model_name: The name of the embedding model to use.

    Returns:
        A list of embeddings, where each embedding is a list of floats.
    """
    aiplatform.init(project=project_id, location=location)

    model = aiplatform.TextEmbeddingModel.from_pretrained(model_name)
    embeddings = model.get_embeddings(document_sections)

    return [embedding.values for embedding in embeddings]

