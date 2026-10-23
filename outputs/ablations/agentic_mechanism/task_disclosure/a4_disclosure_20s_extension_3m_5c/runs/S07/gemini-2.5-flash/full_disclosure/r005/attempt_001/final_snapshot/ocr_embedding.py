from typing import List

import vertexai
from vertexai.language_models import TextEmbeddingInput, TextEmbeddingModel


def embed_document_sections(
    project_id: str, location: str, document_sections: List[str]
) -> List[List[float]]:
    """Embeds document sections for semantic retrieval using Vertex AI's TextEmbeddingModel.

    Args:
        project_id: Your Google Cloud project ID.
        location: The Google Cloud region (e.g., "us-central1").
        document_sections: A list of text strings representing the document sections.

    Returns:
        A list of embeddings, where each embedding is a list of floats.
    """
    vertexai.init(project=project_id, location=location)
    model = TextEmbeddingModel.from_pretrained("textembedding-gecko")
    
    inputs = [TextEmbeddingInput(text, "RETRIEVAL_DOCUMENT") for text in document_sections]
    embeddings = model.get_embeddings(inputs)
    
    return [embedding.values for embedding in embeddings]
