from typing import List, Tuple
from embeddings_client import get_gemini_embeddings_client
from embeddings_models import normalize_batch_embedding_response

def embed_for_search(query: str, documents: List[str]) -> Tuple[List[float], List[List[float]]]:
    """
    Embeds a query and a list of documents for semantic search using Google Gemini Embeddings.
    """
    client = get_gemini_embeddings_client()
    
    # Gemini embeddings API can take a list of content items.
    # The first item will be the query, followed by documents.
    all_content = [query] + documents
    
    response = client.embed_content(model="embedding-001", content=all_content)
    all_embeddings = normalize_batch_embedding_response(response)
    
    query_embedding = all_embeddings[0]
    document_embeddings = all_embeddings[1:]
    
    return query_embedding, document_embeddings

if __name__ == '__main__':
    query_text = "latest research on artificial intelligence"
    document_texts = [
        "A recent paper discusses advancements in neural networks.",
        "The history of AI dates back to the 1950s.",
        "New findings in machine learning algorithms were published last month.",
        "Quantum computing is a rapidly evolving field."
    ]

    query_emb, doc_embs = embed_for_search(query_text, document_texts)

    print(f"Query embedding (first 5 dimensions): {query_emb[:5]}...")
    print(f"Query embedding dimension: {len(query_emb)}")
    print(f"Number of document embeddings: {len(doc_embs)}")
    if doc_embs:
        print(f"First document embedding (first 5 dimensions): {doc_embs[0][:5]}...")
        print(f"First document embedding dimension: {len(doc_embs[0])}")
