from typing import List, Dict
from embeddings_client import initialize_vertexai
from vertexai.language_models import TextEmbeddingModel

def embed_for_search(query: str, documents: List[str]) -> Dict:
    """
    Embeds a query and a list of documents for semantic search using Vertex AI.
    It uses different embedding types for query and documents as recommended.

    Args:
        query: The search query.
        documents: A list of documents to be searched.

    Returns:
        A dictionary containing the query embedding and a list of document embeddings.
    """
    initialize_vertexai()
    
    # Using a specific model from Google Vertex AI with task-specific types
    model = TextEmbeddingModel.from_pretrained("textembedding-gecko@003")
    
    # Embed the query with the 'RETRIEVAL_QUERY' type
    query_embedding = model.get_embeddings(
        [query],
        task_type="RETRIEVAL_QUERY"
    )[0].values
    
    # Embed the documents with the 'RETRIEVAL_DOCUMENT' type
    doc_embeddings = [
        emb.values for emb in model.get_embeddings(
            documents,
            task_type="RETRIEVAL_DOCUMENT"
        )
    ]
    
    return {
        "query_embedding": query_embedding,
        "document_embeddings": doc_embeddings
    }
