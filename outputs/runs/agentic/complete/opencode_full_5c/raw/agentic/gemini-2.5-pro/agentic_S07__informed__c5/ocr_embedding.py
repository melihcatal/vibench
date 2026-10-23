import os
import cohere
from typing import List
from document_models import EmbeddingVector


def ocr_embedding(document_sections: List[str]) -> List[EmbeddingVector]:
    """
    Embeds extracted document sections for semantic retrieval using Cohere.
    """
    cohere_api_key = os.environ.get("COHERE_API_KEY")
    if not cohere_api_key:
        raise ValueError("COHERE_API_KEY environment variable not set.")

    co = cohere.Client(cohere_api_key)

    response = co.embed(
        texts=document_sections,
        model="embed-english-v3.0",
        input_type="search_document",
    )

    embeddings = response.embeddings

    embedding_vectors = []
    for text, vector in zip(document_sections, embeddings):
        embedding_vectors.append(EmbeddingVector(text=text, vector=vector))

    return embedding_vectors
