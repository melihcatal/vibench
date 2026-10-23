import google.generativeai as genai
import os
from typing import List, Dict

def embed_for_search(query: str, documents: List[str]) -> Dict[str, List[List[float]]]:
    """Embeds a query and a list of documents for semantic search using Google Gemini Embeddings.

    Returns a dictionary with 'query_embedding' and 'document_embeddings'.
    """
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = "models/embedding-001"

    query_response = genai.embed_content(model=model, content=query, task_type="RETRIEVAL_QUERY")
    query_embedding = query_response["embedding"]

    document_responses = genai.embed_content(model=model, content=documents, task_type="RETRIEVAL_DOCUMENT")
    document_embeddings = [item["embedding"] for item in document_responses["embeddings"]]

    return {
        "query_embedding": query_embedding,
        "document_embeddings": document_embeddings
    }

if __name__ == '__main__':
    search_query = "best places to visit in summer"
    search_documents = [
        "Summer travel destinations often include beaches and mountains.",
        "Exploring national parks is a great activity for the summer.",
        "Winter sports are popular during colder months.",
        "Many people enjoy hiking and camping when the weather is warm."
    ]

    embeddings_result = embed_for_search(search_query, search_documents)

    print(f"Query embedding (first 5 elements): {embeddings_result["query_embedding"][:5]}...")
    for i, doc_emb in enumerate(embeddings_result["document_embeddings"]):
        print(f"Document {i+1} embedding (first 5 elements): {doc_emb[:5]}...")
