import os
import google.generativeai as genai

def embed_for_search(query: str, documents: list[str]) -> tuple[list[float], list[list[float]]]:
    """
    Embeds a query and a list of documents for semantic search using Google Gemini Embeddings.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")
    
    genai.configure(api_key=api_key)
    
    query_embedding = []
    document_embeddings = []

    try:
        # Embed the query
        query_response = genai.embed_content(
            model="models/embedding-001",
            content=query,
            task_type="RETRIEVAL_QUERY"
        )
        query_embedding = query_response['embeddings'][0]

        # Embed the documents
        # The embed_content function can take a list of strings directly for documents
        document_response = genai.embed_content(
            model="models/embedding-001",
            content=documents,
            task_type="RETRIEVAL_DOCUMENT"
        )
        document_embeddings = document_response['embeddings']

    except Exception as e:
        print(f"Error during embedding for search: {e}")
    
    return query_embedding, document_embeddings

