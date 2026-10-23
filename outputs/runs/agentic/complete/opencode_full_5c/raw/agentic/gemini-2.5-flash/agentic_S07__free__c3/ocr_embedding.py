from typing import List

from document_client import GoogleCloudClients
from document_models import DocumentSectionEmbedding, Embedding


def embed_document_sections(sections: List[str]) -> List[DocumentSectionEmbedding]:
    """Embeds extracted document sections for semantic retrieval using Google Cloud Vertex AI TextEmbeddingModel.

    Args:
        sections: A list of text sections from the document.

    Returns:
        A list of DocumentSectionEmbedding objects, each containing the original text section and its embedding.
    """
    model = GoogleCloudClients.get_vertex_ai_embedding_model()

    # The TextEmbeddingModel can handle a batch of texts
    embeddings = model.get_embeddings(sections)

    document_embeddings: List[DocumentSectionEmbedding] = []
    for i, embedding_result in enumerate(embeddings):
        document_embeddings.append(
            DocumentSectionEmbedding(
                section_text=sections[i],
                embedding=Embedding(values=embedding_result.values),
            )
        )
    return document_embeddings
