from typing import List, Dict, Any
from embeddings_client import get_openai_client


def embed_for_search(
    query: str, documents: List[str], model: str = "text-embedding-3-small"
) -> Dict[str, Any]:
    """
    Embeds a query and a list of documents for semantic search using OpenAI.
    """
    client = get_openai_client()

    # Embed the query
    query_response = client.embeddings.create(input=[query], model=model)
    query_embedding = query_response.data[0].embedding

    # Embed the documents
    doc_response = client.embeddings.create(input=documents, model=model)
    doc_embeddings = [data.embedding for data in doc_response.data]

    return {"query_embedding": query_embedding, "document_embeddings": doc_embeddings}
