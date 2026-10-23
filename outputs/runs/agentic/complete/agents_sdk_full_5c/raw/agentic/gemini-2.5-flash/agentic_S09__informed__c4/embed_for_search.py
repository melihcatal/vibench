import os
import google.generativeai as genai
from embeddings_client import get_embeddings_model

def embed_for_search(query: str, documents: list[str]) -> tuple[list[float], list[list[float]]]:
    """
    Embeds a query and a list of documents for semantic search using the Gemini embeddings model.
    """
    model = get_embeddings_model()

    # The Gemini API supports different tasks for embedding.
    # For search, it's common to embed query and documents separately.
    # We'll use the default general purpose embedding here,
    # but specific models might offer 'QUERY' and 'DOCUMENT' task types.
    
    query_embedding_response = model.embed_content(content=[query])
    query_embedding = query_embedding_response.embeddings[0].values

    document_embeddings_response = model.embed_content(content=documents)
    document_embeddings = [e.values for e in document_embeddings_response.embeddings]

    return query_embedding, document_embeddings

if __name__ == "__main__":
    # Ensure GOOGLE_API_KEY is set in your environment
    search_query = "best hiking trails"
    search_documents = [
        "Explore the beautiful Redwood National Park trails.",
        "Beginner's guide to urban hiking.",
        "Top mountain biking routes in Colorado.",
        "Finding dog-friendly trails near you."
    ]

    query_emb, doc_embs = embed_for_search(search_query, search_documents)

    print(f"Query embedding (first 5 dimensions): {query_emb[:5]}...")
    print(f"Query embedding dimension: {len(query_emb)}")
    print(f"Number of document embeddings: {len(doc_embs)}")
    for i, emb in enumerate(doc_embs):
        print(f"Document {i+1} embedding (first 5 dimensions): {emb[:5]}...")
