import os
import google.generativeai as genai

def embed_for_semantic_search(query: str, documents: list[str]) -> dict:
    """
    Embeds a query and a list of documents for semantic search using Google Gemini Embeddings.
    """
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

    query_embedding_result = genai.embed_content(
        model="models/embedding-001",
        content=[query],
        task_type="RETRIEVAL_QUERY" # Specify task type for query
    )
    query_vector = query_embedding_result["embedding"][0]

    document_embedding_result = genai.embed_content(
        model="models/embedding-001",
        content=documents,
        task_type="RETRIEVAL_DOCUMENT" # Specify task type for documents
    )
    document_vectors = document_embedding_result["embedding"]

    return {
        "query_embedding": query_vector,
        "document_embeddings": document_vectors
    }

if __name__ == '__main__':
    # Example usage (requires GOOGLE_API_KEY environment variable)
    search_query = "latest AI advancements"
    search_documents = [
        "Recent breakthroughs in large language models have been significant.",
        "The use of AI in medical imaging is expanding rapidly.",
        "Quantum computing is a distinct field from artificial intelligence."
    ]

    embeddings = embed_for_semantic_search(search_query, search_documents)
    
    print(f"Query embedding (first 10 dims): {embeddings['query_embedding'][:10]}...")
    print(f"Number of document embeddings: {len(embeddings['document_embeddings'])}")
    if embeddings['document_embeddings']:
        print(f"First document embedding (first 10 dims): {embeddings['document_embeddings'][0][:10]}...")
