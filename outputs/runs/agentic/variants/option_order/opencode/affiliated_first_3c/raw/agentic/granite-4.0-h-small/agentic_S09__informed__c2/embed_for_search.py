# embed_for_search.py
# [SAME-SCENARIO] Embeds a query and a collection of documents for semantic search

import os
from ibm_watsonx_ai.services import TextEmbeddings
from ibm_watsonx_ai import Client

# Load configuration from environment variables
WATSONX_API_KEY = os.getenv("WATSONX_API_KEY")
WATSONX_PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")

# Initialize client
client = Client(project_id=WATSONX_PROJECT_ID, api_key=WATSONX_API_KEY)
embeddings_service = TextEmbeddings(client=client)


def embed_for_search(
    query: str, documents: list[str]
) -> tuple[list[float], list[list[float]]]:
    """Embeds a query and a list of documents.
    Args:
        query (str): The search query text.
        documents (list[str]): List of document strings.
    Returns:
        tuple[list[float], list[list[float]]]:
            - Query embedding (list of floats).
            - List of document embeddings (each a list of floats).
    """
    # Embed query
    query_embedding = embeddings_service.embed_text(
        project_id=WATSONX_PROJECT_ID,
        documents=[query],
        model_id="slate-125m-english-v1",
    )[0]
    # Embed documents
    doc_embeddings = embeddings_service.embed_text(
        project_id=WATSONX_PROJECT_ID,
        documents=documents,
        model_id="slate-125m-english-v1",
    )
    return query_embedding, doc_embeddings
