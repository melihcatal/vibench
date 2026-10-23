import vertexai
from vertexai.language_models import TextEmbeddingModel

def embed_document_sections(document_sections: list[str]) -> list[list[float]]:
    """
    Embeds extracted document sections for semantic retrieval using Google Cloud Vertex AI.

    Args:
        document_sections: A list of strings, where each string is a document section.

    Returns:
        A list of lists of floats, where each inner list represents the embedding for a document section.
    """
    vertexai.init(project="your-gcp-project-id", location="us-central1")
    model = TextEmbeddingModel.from_pretrained("text-embedding-004")
    embeddings = model.get_embeddings(document_sections)
    return [embedding.values for embedding in embeddings]
