import os
from embeddings_client import get_gemini_client

def embed_for_search(query_text: str, document_texts: list[str], model_name: str = "models/text-embedding-004") -> tuple[list[float], list[list[float]]]:
    """
    Embeds a query and a list of documents for semantic search using Google Gemini Embeddings.
    Returns the query embedding and a list of document embeddings.
    """
    genai = get_gemini_client()

    # Embed the query with task_type="RETRIEVAL_QUERY"
    query_response = genai.embed_content(
        model=model_name,
        content=query_text,
        task_type="RETRIEVAL_QUERY"
    )
    query_embedding = query_response['embedding']

    # Embed documents with task_type="RETRIEVAL_DOCUMENT"
    document_response = genai.embed_content(
        model=model_name,
        content=document_texts,
        task_type="RETRIEVAL_DOCUMENT"
    )
    document_embeddings = document_response['embeddings']

    return query_embedding, document_embeddings

if __name__ == '__main__':
    # Example usage (requires GOOGLE_API_KEY environment variable)
    # To run:
    # export GOOGLE_API_KEY='your_api_key_here'
    # python embed_for_search.py
    search_query = "latest developments in AI"
    corpus_documents = [
        "Artificial intelligence is a rapidly evolving field with applications in various industries.",
        "Machine learning, a subset of AI, focuses on algorithms that learn from data.",
        "The history of computing dates back centuries, but modern computers emerged in the 20th century.",
        "Recent breakthroughs in large language models have significantly impacted natural language processing."
    ]

    try:
        query_emb, doc_embs = embed_for_search(search_query, corpus_documents)
        print(f"Query embedding (first 5 dim): {query_emb[:5]}")
        print(f"Query embedding dimension: {len(query_emb)}")
        print(f"\nDocument embeddings for {len(doc_embs)} documents:")
        for i, emb in enumerate(doc_embs):
            print(f"  Doc {i+1} embedding (first 5 dim): {emb[:5]}")
            print(f"  Doc {i+1} embedding dimension: {len(emb)}")

    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
