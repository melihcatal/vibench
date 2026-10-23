from typing import List
from document_client import get_cohere_client


def embed_text_sections(sections: List[str]) -> List[List[float]]:
    """
    Embeds a list of text sections using the Cohere API.
    """
    cohere_client = get_cohere_client()

    response = cohere_client.embed(
        texts=sections, model="embed-english-v3.0", input_type="search_document"
    )
    return response.embeddings
